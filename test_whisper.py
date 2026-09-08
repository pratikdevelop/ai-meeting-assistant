from services.stt.whisper import WhisperService

stt = WhisperService()

audio = stt.record()

text = stt.transcribe(audio)

print("\nTranscript:")
print(text)