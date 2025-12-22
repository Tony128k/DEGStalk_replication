import os
import subprocess
from pathlib import Path

# 输入：指向 dataset/raw_video
INPUT_ROOT = Path("dataset/raw_video")

# 输出：标准化后的视频存放位置
OUTPUT_ROOT = Path("dataset/standardized_video")

TARGET_FPS = 25
TARGET_SIZE = 512

def standardize_video(input_path, output_path):
    os.makedirs(output_path.parent, exist_ok=True)


    filter_cmd = f"fps={TARGET_FPS},scale={TARGET_SIZE}:{TARGET_SIZE}:force_original_aspect_ratio=increase,crop={TARGET_SIZE}:{TARGET_SIZE}"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-vf", filter_cmd,
        "-c:v", "libx264", "-crf", "18", 
        "-c:a", "copy",                  
        "-loglevel", "error",            
        str(output_path)
    ]

    try:
        print(f"处理中: {input_path.name} ...")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_path}: {e}")

def main():
    video_files = list(INPUT_ROOT.rglob("*.mp4"))
    
    print(f"找到 {len(video_files)} 个视频，开始标准化...")

    for vid_path in video_files:
        rel_path = vid_path.relative_to(INPUT_ROOT)
        out_path = OUTPUT_ROOT / rel_path
        
        standardize_video(vid_path, out_path)

    print("\n视频标准化完成")
    print(f"输出路径: {OUTPUT_ROOT.resolve()}")

if __name__ == "__main__":
    main()
