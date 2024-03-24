#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import os
import torch
from random import randint
from core.reconstruct.utils.loss_utils import l1_loss, ssim
from core.reconstruct.gaussian_renderer import render, network_gui
import sys
from core.reconstruct.scene import Scene, GaussianModel
from core.reconstruct.utils.general_utils import safe_state
import uuid
from tqdm import tqdm
from core.reconstruct.utils.image_utils import psnr
from argparse import ArgumentParser, Namespace
from celery.utils.log import get_task_logger
from pathlib import Path 
logger = get_task_logger("celeryApp")
class ModelParams:
    def __init__(self):
        self.sh_degree = 3
        self.source_path = ""
        self.model_path = ""
        self.images = "images" # image path
        self.resolution_schedule = 300 # 每250Iter 更新resolution，直到缩放倍数为1 
        self.num_downscale = 3 
        self.resolution = 1 #像素缩小倍数(loadCam())， -1为默认不缩放,结合colmap可选[1,2,4,8]
        self.white_background = False
        self.data_device = "cuda"
        self.eval = False

class PipelineParams:
    def __init__(self):
        self.convert_SHs_python = False
        self.compute_cov3D_python = False
        self.debug = False

class OptimizationParams:
    def __init__(self):
        self.iterations = 30_000
        self.position_lr_init = 0.00016
        self.position_lr_final = 0.0000016
        self.position_lr_delay_mult = 0.01
        self.position_lr_max_steps = 30_000
        self.feature_lr = 0.0025
        self.opacity_lr = 0.05
        self.scaling_lr = 0.005
        self.rotation_lr = 0.001
        self.percent_dense = 0.01
        self.lambda_dssim = 0.2


        self.opacity_threshold = 0.005 # opacity ; alpha
        self.size_threshold = 20 # threshold of scale for culling(prune) huge gaussians
        self.opacity_reset_interval = 3000

        self.densification_interval = 100
        self.densify_from_iter = 500
        self.densify_until_iter = 15_000
        self.densify_grad_threshold = 0.0002

dataset = ModelParams()
opt = OptimizationParams()
pipe = PipelineParams()

def training(source_path:Path,model_path:Path,uuid:str,debug_from:int=None, saving_iterations:list=[7000,30000]):
    """
    source_path: 原始图像文件夹路径
    model_path: 保存该模型的文件夹路径
    """
    try:
        dataset.source_path = source_path
        dataset.model_path = model_path
        source_path.mkdir(exist_ok=True, parents=True) 
        model_path.mkdir(exist_ok=True, parents=True) 
    except Exception as e:
        raise e 
    first_iter = 1 
    gaussians = GaussianModel(dataset.sh_degree)
    scene = Scene(dataset, gaussians) 
    gaussians.training_setup(opt)
    
    ema_loss_for_log = 0.0
    background = torch.tensor([1,1,1],dtype=torch.float32, device="cuda")
    viewpoint_stack = None 

    for iteration in range(first_iter, opt.iterations+1):

        gaussians.update_learning_rate(iteration)
        
        # Every 1000 iters , increse the levels of SH up to a maximum degree
        if iteration % 1000 == 0:
            gaussians.oneupSHdegree()

        # Pick a random Camera 
        if not viewpoint_stack:
            # dataset.resolution = get_resolution_factor(iteration)
            viewpoint_stack = scene.getTrainCameras(scale=1).copy() # scale 整体缩放
        viewpoint_cam = viewpoint_stack.pop(randint(0,len(viewpoint_stack)-1))

        # Render an image with the viewpoint 
        if (iteration -1) == debug_from:
            pipe.debug = True 
        render_pkg = render(viewpoint_cam, gaussians, pipe, background)
        image, viewspace_point_tensor, visibility_filter, radii = render_pkg["render"], render_pkg["viewspace_points"], render_pkg["visibility_filter"], render_pkg["radii"]

        # Loss
        gt_image = viewpoint_cam.original_image.cuda()
        Ll1 = l1_loss(image, gt_image)
        loss = (1.0 - opt.lambda_dssim) * Ll1 + opt.lambda_dssim * (1.0 - ssim(image, gt_image))
        loss.backward()
        with torch.no_grad():
            ema_loss_for_log = 0.4 * loss.item() + 0.6 * ema_loss_for_log
            if iteration % 5000 == 0:
                logger.info(f"[ITER {iteration}/30000]:{uuid} Loss: {ema_loss_for_log:.{7}f}")

            # Densification
            if iteration < opt.densify_until_iter:
                # Keep track of max radii in image-space for pruning
                gaussians.max_radii2D[visibility_filter] = torch.max(gaussians.max_radii2D[visibility_filter], radii[visibility_filter])
                gaussians.add_densification_stats(viewspace_point_tensor, visibility_filter)

                if iteration > opt.densify_from_iter and iteration % opt.densification_interval == 0:
                    size_threshold = 20 if iteration > opt.opacity_reset_interval else None
                    gaussians.densify_and_prune(opt.densify_grad_threshold, 
                                                opt.opacity_threshold, 
                                                scene.cameras_extent, 
                                                size_threshold)
                
                if iteration % opt.opacity_reset_interval == 0 or (dataset.white_background and iteration == opt.densify_from_iter):
                    gaussians.reset_opacity()

            # Optimizer step
            if iteration < opt.iterations:
                gaussians.optimizer.step()
                gaussians.optimizer.zero_grad(set_to_none = True)

        
        if (iteration in saving_iterations):
            logger.info("\n[ITER {}] Saving Gaussians".format(iteration))
            scene.save(iteration,uuid=uuid) 
        torch.cuda.empty_cache()

def get_resolution_factor(iteration):
        # iters [0,249] 8; [250,499] 4; [500,749] 2; [750,end] -1  
        if iteration < 3*dataset.resolution_schedule:
            return 2 ** max(
                (dataset.num_downscale - iteration // dataset.resolution_schedule),
                0,
            )
        else:
            return 1

if __name__ == "__main__":
    pass
