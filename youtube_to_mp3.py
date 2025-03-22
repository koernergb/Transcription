#!/usr/bin/env python3
import os
import argparse
from pytube import YouTube
import ffmpeg

def download_youtube_as_mp3(url, output_path=None):
    """
    Download a YouTube video and convert it to MP3.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the MP3 file (default: current directory)
    
    Returns:
        str: Path to the downloaded MP3 file
    """
    try:
        # Create output directory if it doesn't exist
        if output_path and not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Get the YouTube video
        print(f"Fetching video from {url}...")
        yt = YouTube(url)
        
        # Get video title for filename
        video_title = yt.title
        safe_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        
        # Get the audio stream with highest quality
        print("Extracting audio stream...")
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        # Download the audio
        print("Downloading audio...")
        temp_file = audio_stream.download(output_path=output_path or ".", filename=f"{safe_title}_temp")
        
        # Convert to MP3 using ffmpeg
        print("Converting to MP3...")
        output_file = os.path.join(output_path or ".", f"{safe_title}.mp3")
        
        # Use ffmpeg to convert to MP3
        ffmpeg.input(temp_file).output(output_file, acodec='libmp3lame', q='0').run(quiet=True, overwrite_output=True)
        
        # Remove the temporary file
        os.remove(temp_file)
        
        print(f"Download complete: {output_file}")
        return output_file
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube video as MP3")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", help="Output directory path")
    
    args = parser.parse_args()
    download_youtube_as_mp3(args.url, args.output)
