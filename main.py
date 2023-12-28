from pytube import YouTube
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich import box
from rich.progress import Progress

import sys
import argparse
import os

def Check_Option(option):
    return True if option.lower() == "y" else False

def Create_Table(streams, is_audio):
    table = Table(title="Video Options", box=box.ROUNDED, header_style="bold magenta")
    columns =  ["ID", "ABR"] if is_audio else ["ID", "Resolution", "FPS"]

    filtered_streams = streams.filter(only_audio=True) if is_audio else streams.filter(file_extension='mp4', progressive=True)

    for column in columns:
        table.add_column(column, justify="center")

    for item in filtered_streams:
        table.add_row(
                str(item.itag),
                str(item.abr),
            ) if is_audio else table.add_row(
                str(item.itag),
                str(item.resolution),
                str(item.fps),
            )

    console = Console()

    console.print(table)

def Download_Video(stream, chunk, bytes_remaining):
    with Progress() as progress:
        task = progress.add_task("Downloading Video...", total=stream.filesize)

        while not progress.finished:
            progress.update(task, completed=stream.filesize - bytes_remaining, refresh=True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script used for download youtube videos/audios")
    parser.add_argument("--url", help="The Url of the Youtube Video")
    parser.add_argument("--onlyaudio", help="Write this flag if you want only the audio of the video", action=argparse.BooleanOptionalAction)
    args = parser.parse_args(sys.argv[1:])

    yt_video = YouTube(args.url, on_progress_callback=Download_Video)

    rprint(f"Are you going to download \n[italic magenta]:link:[link={args.url}]{yt_video.title}[/link][/italic magenta]\nContinue?: [bold green] [Y]: Yes [/bold green][bold red] [N]: No [/bold red]")

    if Check_Option(input()) == False:
        sys.exit()

    

    Create_Table(yt_video.streams, args.onlyaudio)

    rprint("[italic]Select by :id_button:[red blink]ID[/red blink] what do you want to download[/italic]")

    id_value = input()

    stream = yt_video.streams.get_by_itag(int(id_value))

    path_file = stream.download()

    if args.onlyaudio:
        pre, ext = os.path.splitext(path_file)
        os.rename(path_file, pre + ".mp3")