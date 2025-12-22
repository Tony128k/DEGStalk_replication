import os
import subprocess
import sys

def check_ffmpeg():
    """检查FFmpeg是否安装并配置到环境变量"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误：未检测到FFmpeg，请先安装并添加到系统环境变量！")
        sys.exit(1)

def extract_frames_and_audio(input_video_dir, output_root_dir):
    """
    提取视频帧和音频
    :param input_video_dir: 标准化视频文件夹路径（dataset/standardized_video）
    :param output_root_dir: 输出根目录（dataset/final_result）
    """
    
    print(f"正在扫描目录: {input_video_dir} ...")
    
    video_extensions = (".mp4", ".avi", ".mov", ".mkv")
    found_any = False

    for root, dirs, files in os.walk(input_video_dir):
        for video_filename in files:
            if not video_filename.lower().endswith(video_extensions):
                continue
            
            found_any = True
            
            # 1. 定义路径
            input_video_path = os.path.join(root, video_filename)
            
            # 获取视频名作为输出文件夹名
            video_basename = os.path.splitext(video_filename)[0]
            
            # 输出路径：dataset/final_result/VideoName
            output_video_dir = os.path.join(output_root_dir, video_basename)
            output_images_dir = os.path.join(output_video_dir, "images")
            output_audio_path = os.path.join(output_video_dir, "audio.wav")

            # 2. 创建输出目录
            os.makedirs(output_images_dir, exist_ok=True)

            print(f"\n正在处理: {video_basename}")

            # 3. 提取帧序列
            frame_cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-r", "25",
                "-f", "image2",
                "-start_number", "0",          
                "-q:v", "2",                    
                os.path.join(output_images_dir, "%05d.jpg")
            ]
            
            try:
                subprocess.run(frame_cmd, check=True, capture_output=True, text=True)
                print(f"   [Frames] 提取成功 -> images/")
            except subprocess.CalledProcessError as e:
                print(f"   [Error] 帧提取失败: {e.stderr}")
                continue

            # 4. 提取音频
            audio_cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                output_audio_path
            ]
            
            try:
                subprocess.run(audio_cmd, check=True, capture_output=True, text=True)
                print(f"   [Audio]  提取成功 -> audio.wav")
            except subprocess.CalledProcessError as e:
                print(f"   [Error] 音频提取失败: {e.stderr}")

    if not found_any:
        print("未找到任何视频文件，请检查 dataset/standardized_video 结构！")

if __name__ == "__main__":
    check_ffmpeg()
    
    # 路径配置
    INPUT_VIDEO_DIR = "dataset/standardized_video" 
    OUTPUT_ROOT_DIR = "dataset/final_result"     
    
    if not os.path.exists(INPUT_VIDEO_DIR):
        print(f"错误：输入文件夹 {INPUT_VIDEO_DIR} 不存在！")
        sys.exit(1)
    
    extract_frames_and_audio(INPUT_VIDEO_DIR, OUTPUT_ROOT_DIR)
    print("\n所有任务完成！")