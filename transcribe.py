import whisper
import sys
import torch

def transcribe_audio(audio_path, output_path):
    try:
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        # Load the Whisper model (using the base model for faster processing)
        print("Loading Whisper model...")
        model = whisper.load_model("base").to(device)
        
        # Transcribe the audio file
        print(f"Transcribing {audio_path}...")
        # If using CPU, explicitly set fp16=False to avoid warnings
        result = model.transcribe(
            audio_path,
            fp16=False if device == "cpu" else True
        )
        
        # Save the transcription to a text file
        print(f"Saving transcription to {output_path}...")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        print("Transcription complete!")
        
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transcribe.py <input_audio_file> <output_text_file>")
        sys.exit(1)
        
    audio_path = sys.argv[1]
    output_path = sys.argv[2]
    
    transcribe_audio(audio_path, output_path)
