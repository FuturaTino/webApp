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