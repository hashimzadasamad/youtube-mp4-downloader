import os
import subprocess
import sys

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✅ FFmpeg is installed.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg is not installed or not in PATH.")
        return False

def check_yt_dlp():
    """Check if yt-dlp is installed."""
    try:
        subprocess.run(["yt-dlp", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✅ yt-dlp is installed.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp is not installed. Installing now...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=True)
        return check_yt_dlp()

def download_youtube_video(url, output_path="."):
    """Download the best video and audio from YouTube and merge them using FFmpeg."""
    if not check_yt_dlp():
        print("❌ yt-dlp installation failed.")
        return
    
    if not check_ffmpeg():
        print("⚠️ Please install FFmpeg and ensure it's in your system PATH.")
        return

    try:
        print("🔽 Downloading video and audio...")
        subprocess.run([
            "yt-dlp",
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),
            url
        ], check=True)
        print("✅ Download and merging complete!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during download: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ").strip()
    download_youtube_video(video_url)
