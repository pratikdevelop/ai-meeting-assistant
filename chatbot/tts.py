import numpy as np
import sounddevice as sd

from kokoro import KPipeline


class KokoroTTS:

    def __init__(
        self,
        voice="af_heart",
        speed=1.0,
        sample_rate=24000,
    ):
        print("🧠 Loading Kokoro TTS...")

        self.pipeline = KPipeline(
            lang_code="a",
            repo_id="hexgrad/Kokoro-82M",
        )

        self.voice = voice
        self.speed = speed
        self.sample_rate = sample_rate

        print("✅ Kokoro TTS loaded")

    def generate(self, text: str):

        if not text or not text.strip():
            return None

        audio_chunks = []

        generator = self.pipeline(
            text,
            voice=self.voice,
            speed=self.speed,
        )

        for _, _, audio in generator:
            audio_chunks.append(audio)

        if not audio_chunks:
            return None

        return np.concatenate(
            audio_chunks
        )

    def speak(self, text: str):

        audio = self.generate(text)

        if audio is None:
            return

        sd.play(
            audio,
            self.sample_rate,
        )

        sd.wait()

    def stop(self):
        sd.stop()