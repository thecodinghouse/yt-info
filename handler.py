import sieve
from typing import Literal

metadata = sieve.Metadata(
    description="Download highest-resolution version of YouTube video as an MP4.",
    code_url="https://github.com/sieve-community/examples/blob/main/youtube_downloader",
    image=sieve.Image(
        url="https://yt3.googleusercontent.com/584JjRp5QMuKbyduM_2k5RlXFqHJtQ0qLIPZpwbUjMJmgzZngHcam5JMuZQxyzGMV5ljwJRl0Q=s900-c-k-c0x00ffffff-no-rj"
    ),
    tags=["Video"],
   # readme=open("README.md", "r").read(),
)


@sieve.function(
    name="youtube_info",
    # system_packages=["ffmpeg"],
    python_packages=[
        "pytube @ git+https://github.com/sieve-community/pytube.git",
    ],
    metadata=metadata
)
def download(
    url: str,
    resolution: Literal["highest-available", "lowest-available", "1080p", "720p", "480p", "360p", "240p", "144p"] = "1080p",
):
    '''
    :param url: YouTube URL to download
    :param resolution: The resolution of the video to download. If the desired resolution is not available, the closest resolution will be downloaded instead.
    :param include_audio: Whether to include audio in the video.
    :return: The downloaded YouTube video
    '''
    from pytube import YouTube
    import time

    print("setting stream...")
    data = {}

    #print("filtering stream for highest quality mp4...")
    stream_tries = 10
    while stream_tries > 0:
        try:
            yt = YouTube(url)
            data["title"] = yt.title
            data["duration"] = yt.length
            if yt.description:
                data["description"] = yt.description
            if yt.thumbnail_url:
                data["poster_url"] = yt.thumbnail_url

            all_streams = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc() #.first()
            video = [stream for stream in all_streams if stream.video_codec.startswith('avc1')]
            break
        except Exception as e:
            print(f"Error filtering stream: {e}")
            stream_tries -= 1
            time.sleep(0.3)
            if stream_tries == 0:
                raise e
            
    if resolution == "highest-available":
        video = video[0]
        print(f"highest available resolution is {video.resolution}...")
    elif resolution == "lowest-available":
        video = video[-1]
        print(f"lowest available resolution is {video.resolution}...")
    else:
        desired_res = int(resolution.replace('p', ''))
        diff_list = [(abs(desired_res - int(stream.resolution.replace('p', ''))), stream) for stream in video]
        diff_list.sort(key=lambda x: x[0])
        video = diff_list[0][1]
        if video.resolution != resolution:
            print(f"{resolution} resolution is not available, using {video.resolution} instead...")
        else:
            print(f"selected resolution is {resolution}...")

        
    print('getting file size...')
    data["file_size"] = video.filesize

    return data