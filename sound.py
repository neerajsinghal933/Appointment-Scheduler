import whisper
import sounddevice as sd
import numpy as np
import queue
import scipy.io.wavfile as wav
import tempfile
import time
import os

# Parameters
sample_rate = 16000
silence_threshold = 0.01  # Adjust this value if needed
max_silence_duration = 3.0  # seconds

# Setup
audio_queue = queue.Queue()
recording = []
silent_start = None

def callback(indata, frames, time_info, status):
    volume_norm = np.linalg.norm(indata) / len(indata)
    audio_queue.put((indata.copy(), volume_norm))

print("🎙️ Speak now. Recording will stop after 3 seconds of silence...")

with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
    start_time = time.time()
    while True:
        try:
            indata, volume = audio_queue.get(timeout=0.5)
            recording.append(indata)

            # Debug: Print volume
            # print(f"Volume: {volume:.4f}")

            if volume < silence_threshold:
                if silent_start is None:
                    silent_start = time.time()
                elif time.time() - silent_start > max_silence_duration:
                    print("⏹️ Detected silence. Stopping recording...")
                    break
            else:
                silent_start = None  # Reset silence timer when sound comes
        except queue.Empty:
            continue

# Save recording to WAV
recorded_audio = np.concatenate(recording, axis=0)
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
    wav.write(tmpfile.name, sample_rate, recorded_audio)
    temp_filename = tmpfile.name

print(f"✅ Audio saved at: {temp_filename}")

# Transcribe using Whisper
model = whisper.load_model("base")
result = model.transcribe(temp_filename)
print("📝 Transcription:\n", result["text"])

# Optionally delete temp file
os.remove(temp_filename)
