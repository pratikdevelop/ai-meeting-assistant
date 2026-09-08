import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")

        self.model = os.getenv(
            "MODEL",
            "openai/gpt-oss-120b",
        )

        self.whisper_model = os.getenv(
            "WHISPER_MODEL",
            "whisper-large-v3",
        )

        self.debug = (
            os.getenv("DEBUG", "False").lower() == "true"
        )

        # Audio
        self.audio_sample_rate = int(
            os.getenv("AUDIO_SAMPLE_RATE", "16000")
        )

        self.vad_mode = int(
            os.getenv("VAD_MODE", "2")
        )

        self.vad_silence_ms = int(
            os.getenv("VAD_SILENCE_MS", "800")
        )

        self.vad_start_timeout_ms = int(
            os.getenv("VAD_START_TIMEOUT_MS", "8000")
        )

        self.max_recording_seconds = int(
            os.getenv("MAX_RECORDING_SECONDS", "15")
        )

    def validate(self):
        if not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env"
            )

        if not 0 <= self.vad_mode <= 3:
            raise ValueError(
                "VAD_MODE must be between 0 and 3"
            )


settings = Settings()
settings.validate()