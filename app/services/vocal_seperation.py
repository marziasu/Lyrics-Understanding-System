import os
import subprocess
import sys
from pathlib import Path

def run_demucs_separation(audio_file, model="htdemucs", two_stems=True, output_dir="separated"):
    """
    Run Demucs separation using subprocess
    """
    print(f"Starting Demucs separation for: {audio_file}")
    
    # Build command
    cmd = [
        sys.executable, "-m", "demucs.separate",
        "--out", output_dir,
        "-n", model
    ]
    
    if two_stems:
        cmd.extend(["--two-stems", "vocals"])
    
    cmd.append(audio_file)
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        # Run Demucs
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Demucs separation completed successfully!")
        print(result.stdout)
        
        # Find output files
        audio_name = Path(audio_file).stem
        model_dir = os.path.join(output_dir, model, audio_name)
        
        if two_stems:
            vocals_file = os.path.join(model_dir, "vocals.wav")
            no_vocals_file = os.path.join(model_dir, "no_vocals.wav")
            return vocals_file, no_vocals_file
        else:
            vocals_file = os.path.join(model_dir, "vocals.wav")
            drums_file = os.path.join(model_dir, "drums.wav")
            bass_file = os.path.join(model_dir, "bass.wav")
            other_file = os.path.join(model_dir, "other.wav")
            return vocals_file, drums_file, bass_file, other_file
            
    except subprocess.CalledProcessError as e:
        print(f"Error running Demucs: {e}")
        print(f"Error output: {e.stderr}")
        return None

# Example usage
if __name__ == "__main__":
    from app.config import AUDIO_DIR
    audio_file = os.path.join(AUDIO_DIR, "Niye Jabe Ki.mp3")
    
    vocals, instrumental = run_demucs_separation(
        audio_file,
        model="htdemucs",
        two_stems=True,
        output_dir="demucs_output"
    )
    
    print(f"Separated vocals: {vocals}")
    print(f"Separated instrumental: {instrumental}")
