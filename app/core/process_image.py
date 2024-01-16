from typing import List, Tuple, Optional
from pathlib import Path
import shutil
import sys
import math
import subprocess
from rich.console import Console
import re 
import logging
import os 
CONSOLE = Console(width=120)
def run_command(cmd: str, verbose=False) -> Optional[str]:
    """Runs a command and returns the output.

    Args:
        cmd: Command to run.
        verbose: If True, logs the output of the command.
    Returns:
        The output of the command if return_output is True, otherwise None.
    """
    out = subprocess.run(cmd, capture_output=not verbose, shell=True, check=False)
    if out.returncode != 0:
        CONSOLE.rule("[bold red] :skull: :skull: :skull: ERROR :skull: :skull: :skull: ", style="red")
        CONSOLE.print(f"[bold red]Error running command: {cmd}")
        CONSOLE.rule(style="red")
        CONSOLE.print(out.stderr.decode("utf-8"))
        sys.exit(1)
    if out.stdout is not None:
        return out.stdout.decode("utf-8")
    return out

def get_num_frames_in_video(video: Path) -> int:
    """Returns the number of frames in a video.

    Args:
        video: Path to a video.

    Returns:
        The number of frames in a video.
    """
    cmd = f'ffprobe -v error -select_streams v:0 -count_packets \
            -show_entries stream=nb_read_packets -of csv=p=0 "{video}"'
    output = run_command(cmd)
    assert output is not None
    number_match = re.search(r"\d+", output)
    assert number_match is not None
    return int(number_match[0])


def convert_video_to_images(
    video_path: Path,
    image_dir: Path,
    num_frames_target: int,
    num_downscales: int,
    crop_factor: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
    verbose: bool = False,
    image_prefix: str = "frame_",
    keep_image_dir: bool = False,
) -> Tuple[List[str], int]:
    """Converts a video into a sequence of images.

    Args:
        video_path: Path to the video.
        output_dir: Path to the output directory.
        num_frames_target: Number of frames to extract.
        num_downscales: Number of times to downscale the images. Downscales by 2 each time.
        crop_factor: Portion of the image to crop. Should be in [0,1] (top, bottom, left, right)
        verbose: If True, logs the output of the command.
        image_prefix: Prefix to use for the image filenames.
        keep_image_dir: If True, don't delete the output directory if it already exists.
    Returns:
        A tuple containing summary of the conversion and the number of extracted frames.
    """

    # If keep_image_dir is False, then remove the output image directory and its downscaled versions
    if not keep_image_dir:
        for i in range(num_downscales + 1):
            dir_to_remove = image_dir if i == 0 else f"{image_dir}_{2**i}"
            shutil.rmtree(dir_to_remove, ignore_errors=True)
    image_dir.mkdir(exist_ok=True, parents=True)

    for i in crop_factor:
        if i < 0 or i > 1:
            CONSOLE.print("[bold red]Error: Invalid crop factor. All crops must be in [0,1].")
            sys.exit(1)

    if video_path.is_dir():
        CONSOLE.print(f"[bold red]Error: Video path is a directory, not a path: {video_path}")
        sys.exit(1)
    if video_path.exists() is False:
        CONSOLE.print(f"[bold red]Error: Video does not exist: {video_path}")
        sys.exit(1)


    num_frames = get_num_frames_in_video(video_path)
    if num_frames == 0:
        CONSOLE.print(f"[bold red]Error: Video has no frames: {video_path}")
        sys.exit(1)
    CONSOLE.print("Number of frames in video:", num_frames)

    ffmpeg_cmd = f'ffmpeg -i "{video_path}"'

    crop_cmd = ""
    if crop_factor != (0.0, 0.0, 0.0, 0.0):
        height = 1 - crop_factor[0] - crop_factor[1]
        width = 1 - crop_factor[2] - crop_factor[3]
        start_x = crop_factor[2]
        start_y = crop_factor[0]
        crop_cmd = f"crop=w=iw*{width}:h=ih*{height}:x=iw*{start_x}:y=ih*{start_y},"

    spacing = num_frames // num_frames_target

    downscale_chains = [f"[t{i}]scale=iw/{2**i}:ih/{2**i}[out{i}]" for i in range(num_downscales + 1)]
    downscale_dirs = [Path(str(image_dir) + (f"_{2**i}" if i > 0 else "")) for i in range(num_downscales + 1)]
    downscale_paths = [downscale_dirs[i] / f"{image_prefix}%05d.png" for i in range(num_downscales + 1)]

    for dir in downscale_dirs:
        dir.mkdir(parents=True, exist_ok=True)

    downscale_chain = (
        f"split={num_downscales + 1}"
        + "".join([f"[t{i}]" for i in range(num_downscales + 1)])
        + ";"
        + ";".join(downscale_chains)
    )

    ffmpeg_cmd += " -vsync vfr"

    if spacing > 1:
        CONSOLE.print("Number of frames to extract:", math.ceil(num_frames / spacing))
        select_cmd = f"thumbnail={spacing},setpts=N/TB,"
    else:
        CONSOLE.print("[bold red]Can't satisfy requested number of frames. Extracting all frames.")
        ffmpeg_cmd += " -pix_fmt bgr8"
        select_cmd = ""

    downscale_cmd = f' -filter_complex "{select_cmd}{crop_cmd}{downscale_chain}"' + "".join(
        [f' -map "[out{i}]" "{downscale_paths[i]}"' for i in range(num_downscales + 1)]
    )

    ffmpeg_cmd += downscale_cmd

    run_command(ffmpeg_cmd, verbose=verbose)

    num_final_frames = len(list(image_dir.glob("*.png")))
    summary_log = []
    summary_log.append(f"Starting with {num_frames} video frames")
    summary_log.append(f"We extracted {num_final_frames} images with prefix '{image_prefix}'")
    CONSOLE.log("[bold green]:tada: Done converting video to images.")
    return summary_log, num_final_frames

def convert_images_to_colmap(source_path:str,camera:str="OPENCV",no_gpu:bool=False,skip_matching:bool=False,colmap_executable:str="",resize:bool=True,magick_executable:str="",verbose:bool=False):


    colmap_command = '"{}"'.format(colmap_executable) if len(colmap_executable) > 0 else "colmap"
    magick_command = '"{}"'.format(magick_executable) if len(magick_executable) > 0 else "magick"
    use_gpu = 1 if not no_gpu else 0

    if not skip_matching:
        os.makedirs(source_path + "/distorted/sparse", exist_ok=True)

        ## Feature extraction
        feat_extracton_cmd = colmap_command + " feature_extractor "\
            "--database_path " + source_path + "/distorted/database.db \
            --image_path " + source_path + "/input \
            --ImageReader.single_camera 1 \
            --ImageReader.camera_model " + camera + " \
            --SiftExtraction.use_gpu " + str(use_gpu)
        run_command(feat_extracton_cmd, verbose=verbose)

        ## Feature matching
        feat_matching_cmd = colmap_command + " exhaustive_matcher \
            --database_path " + source_path + "/distorted/database.db \
            --SiftMatching.use_gpu " + str(use_gpu)
        run_command(feat_matching_cmd, verbose=verbose)

        ### Bundle adjustment
        # The default Mapper tolerance is unnecessarily large,
        # decreasing it speeds up bundle adjustment steps.
        mapper_cmd = (colmap_command + " mapper \
            --database_path " + source_path + "/distorted/database.db \
            --image_path "  + source_path + "/input \
            --output_path "  + source_path + "/distorted/sparse \
            --Mapper.ba_global_function_tolerance=0.000001")
        run_command(mapper_cmd, verbose=verbose)

    ### Image undistortion
    ## We need to undistort our images into ideal pinhole intrinsics.
    img_undist_cmd = (colmap_command + " image_undistorter \
        --image_path " + source_path + "/input \
        --input_path " + source_path + "/distorted/sparse/0 \
        --output_path " + source_path + "\
        --output_type COLMAP")
    run_command(img_undist_cmd, verbose=verbose)

    files = os.listdir(source_path + "/sparse")
    os.makedirs(source_path + "/sparse/0", exist_ok=True)
    # Copy each file from the source directory to the destination directory

    for file in files:
        if file == '0':
            continue
        source_file = os.path.join(source_path, "sparse", file)
        destination_file = os.path.join(source_path, "sparse", "0", file)
        shutil.move(source_file, destination_file)

    if(resize):
        print("Copying and resizing...")

        # Resize images.
        os.makedirs(source_path + "/images_2", exist_ok=True)
        os.makedirs(source_path + "/images_4", exist_ok=True)
        os.makedirs(source_path + "/images_8", exist_ok=True)
        # Get the list of files in the source directory
        files = os.listdir(source_path + "/images")
        # Copy each file from the source directory to the destination directory
        for file in files:
            source_file = os.path.join(source_path, "images", file)

            destination_file = os.path.join(source_path, "images_2", file)
            shutil.copy2(source_file, destination_file)
            exit_code = os.system(magick_command + " mogrify -resize 50% " + destination_file)
            if exit_code != 0:
                logging.error(f"50% resize failed with code {exit_code}. Exiting.")
                exit(exit_code)

            destination_file = os.path.join(source_path, "images_4", file)
            shutil.copy2(source_file, destination_file)
            exit_code = os.system(magick_command + " mogrify -resize 25% " + destination_file)
            if exit_code != 0:
                logging.error(f"25% resize failed with code {exit_code}. Exiting.")
                exit(exit_code)

            destination_file = os.path.join(source_path, "images_8", file)
            shutil.copy2(source_file, destination_file)
            exit_code = os.system(magick_command + " mogrify -resize 12.5% " + destination_file)
            if exit_code != 0:
                logging.error(f"12.5% resize failed with code {exit_code}. Exiting.")
                exit(exit_code)

    print("Done.")




if __name__ =="__main__":
    video_path = Path('D:\Repo\webApp\eraLi.mp4')
    image_dir = Path(fr'D:\Repo\webApp\app\storage\auoiqwe-ajlkasdu\images')
    convert_video_to_images(video_path,image_dir,300,0)