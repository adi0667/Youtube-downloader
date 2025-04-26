from pytube import YouTube


def download_video(url, save_path='.'):
    try:
        # Create YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()

        # Download the video
        print(f'Downloading: {yt.title}')
        stream.download(output_path=save_path)
        print('Download complete!')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    # Example URL
    url = input("Enter the YouTube video URL: ")
    save_path = input("Enter the folder path to save the video (default is current directory): ") or '.'
    download_video(url, save_path)
