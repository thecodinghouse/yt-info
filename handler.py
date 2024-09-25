import sieve
from typing import Literal

metadata = sieve.Metadata(
    title = "YouTube Video Downloader",
    description="Download YouTube videos in MP4 format at any resolution.",
    code_url="https://github.com/sieve-community/examples/blob/main/youtube_downloader",
    image=sieve.Image(
        url="https://yt3.googleusercontent.com/584JjRp5QMuKbyduM_2k5RlXFqHJtQ0qLIPZpwbUjMJmgzZngHcam5JMuZQxyzGMV5ljwJRl0Q=s900-c-k-c0x00ffffff-no-rj"
    ),
    tags=["Video"],
    # readme=open("README.md", "r").read(),
)

@sieve.function(
    name="youtube_info",
    system_packages=["ffmpeg"],
    python_packages=["yt-dlp", "pytube"],
    metadata=metadata,
)
def download(
    url: str,
    resolution: Literal["highest-available", "lowest-available", "1080p", "720p", "480p", "360p", "240p", "144p"] = "1080p",
    include_audio: bool = True,
):
    '''
    :param url: YouTube URL to download
    :param resolution: The resolution of the video to download. If the desired resolution is not available, the closest resolution will be downloaded instead.
    :param include_audio: Whether to include audio in the video.
    :return: The downloaded YouTube video
    '''
    import yt_dlp
    import os

    # output_filename = "output.mp4"

    # if os.path.exists(output_filename):
    #     print("Deleting existing output file...")
    #     os.remove(output_filename)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4][vcodec^=avc1]/best',
        # 'outtmpl': output_filename,
        'quiet': True,  # Suppress output
        'no_warnings': True,  # Suppress warnings
        'noprogress': True,  # Disable progress bar
    }

    if resolution != "highest-available":
        if resolution == "lowest-available":
            ydl_opts['format'] = 'worstvideo[ext=mp4][vcodec^=avc1]+worstaudio[ext=m4a]/worst[ext=mp4][vcodec^=avc1]/worst'
        else:
            ydl_opts['format'] = f'bestvideo[height<={resolution[:-1]}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<={resolution[:-1]}][ext=mp4][vcodec^=avc1]/best'

    if not include_audio:
        ydl_opts['format'] = ydl_opts['format'].split('+')[0]

    print("Downloading video...")
    data = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        data["title"] = info_dict.get('title', None) 
        data["duration"] = info_dict.get('duration', None)
        data["description"] = info_dict.get('description', None)
        data["poster_url"] = info_dict.get('thumbnail', None)
        # data["poster_url"] = info_dict.get('thumbnails', [{}])[0].get('url', None)
        data["file_size"] = info_dict.get('requested_formats', [{}])[0].get('filesize', None)


    print('Done!')
    return data
    # return sieve.File(path=output_filename)

# if __name__ == "__main__":
#    download("https://www.youtube.com/watch?v=AKJfakEsgy0")