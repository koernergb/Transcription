#!/usr/bin/env python3
import os
import argparse
import ffmpeg

def convert_mp4_to_mp3(input_file, output_file=None):
    """
    Convert an MP4 file to MP3 format.
    
    Args:
        input_file (str): Path to input MP4 file
        output_file (str, optional): Path for output MP3 file. If not provided,
                                   will use the same name as input with .mp3 extension
    
    Returns:
        str: Path to the output MP3 file
    """
    try:
        # Verify input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        # If no output file specified, create one with same name but .mp3 extension
        if output_file is None:
            output_file = os.path.splitext(input_file)[0] + '.mp3'
            
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        print(f"Converting {input_file} to MP3...")
        
        # Convert to MP3 using ffmpeg with good quality settings
        ffmpeg.input(input_file).output(
            output_file,
            acodec='libmp3lame',  # Use MP3 codec
            q='0',                # Highest quality
            map='0:a'            # Only copy audio stream
        ).run(quiet=True, overwrite_output=True)
        
        print(f"Conversion complete! MP3 saved as: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert MP4 video to MP3 audio")
    parser.add_argument("input", help="Input MP4 file path")
    parser.add_argument("-o", "--output", help="Output MP3 file path (optional)")
    
    args = parser.parse_args()
    convert_mp4_to_mp3(args.input, args.output) 