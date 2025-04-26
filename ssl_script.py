import yt_dlp
import os

def download_video(url, save_path='.'): 
    try:
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'cookies': 'cookies.txt',  # Use cookies for authentication
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            info = ydl.extract_info(url, download=True)
            ext = info.get('ext', 'mp4')
            title = info.get('title', 'video')
            filename = f"{title}.{ext}"
            return os.path.join(save_path, filename)
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == '__main__':
    url = input("Enter the YouTube video URL: ")
    save_path = input("Enter the folder path to save the video (default is current directory): ") or '.'
    download_video(url, save_path)
