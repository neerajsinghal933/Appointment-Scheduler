import whisper

model = whisper.load_model("base")  # You can use "tiny", "small", "medium", or "large"
result = model.transcribe("testing.mp3")
print(result["text"])