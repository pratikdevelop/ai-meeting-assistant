from services.stt.whisper import WhisperService


class VoiceInputProcessor:

    def __init__(self):
        self.whisper = WhisperService()

    def listen(self):

        filename = self.whisper.record()

        if filename is None:
            return ""

        text = self.whisper.transcribe(
            filename
        )

        if not text:
            return ""

        print(f"\nYou: {text}")

        # Ignore punctuation-only results.
        cleaned = text.strip()

        if not cleaned:
            return ""

        if all(
            char in ".,!?;:'\"…- "
            for char in cleaned
        ):
            print(
                "⚠️ Ignoring punctuation-only transcription."
            )
            return ""

        return cleaned