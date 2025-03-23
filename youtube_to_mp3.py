#!/usr/bin/env python3
import os
import argparse
from pytube import YouTube
import ffmpeg
import time

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
        
        # Add retry mechanism
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"Attempt {retry_count + 1}: Fetching video from {url}...")
                # Initialize YouTube with custom parameters
                yt = YouTube(
                    url,
                    use_oauth=False,
                    allow_oauth_cache=True
                )
                
                # Get video title for filename
                video_title = yt.title
                safe_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                
                print(f"Found video: {video_title}")
                
                # Get the audio stream with highest quality
                print("Extracting audio stream...")
                audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                
                if not audio_stream:
                    raise Exception("No suitable audio stream found")
                
                # Download the audio
                print("Downloading audio...")
                temp_file = audio_stream.download(output_path=output_path or ".", filename=f"{safe_title}_temp")
                
                # Convert to MP3 using ffmpeg
                print("Converting to MP3...")
                output_file = os.path.join(output_path or ".", f"{safe_title}.mp3")
                
                # Use ffmpeg to convert to MP3
                ffmpeg.input(temp_file).output(output_file, acodec='libmp3lame', q='0').run(quiet=True, overwrite_output=True)
                
                # Remove the temporary file
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                print(f"Download complete: {output_file}")
                return output_file
                
            except Exception as e:
                print(f"Attempt {retry_count + 1} failed with error: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    raise Exception(f"Failed after {max_retries} attempts: {str(e)}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube video as MP3")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", help="Output directory path")
    
    args = parser.parse_args()
    download_youtube_as_mp3(args.url, args.output)
