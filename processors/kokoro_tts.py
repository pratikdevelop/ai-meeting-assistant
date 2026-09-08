import asyncio

from pipecat.frames.frames import (
    LLMFullResponseEndFrame,
    LLMFullResponseStartFrame,
    LLMTextFrame,
)

from pipecat.processors.frame_processor import (
    FrameDirection,
    FrameProcessor,
)

from chatbot.tts import KokoroTTS


class KokoroTTSProcessor(FrameProcessor):

    def __init__(self):
        super().__init__()

        print(
            "🧠 Initializing Kokoro TTS processor..."
        )

        self.tts = KokoroTTS()

        self.response_text = ""

        # Runner uses this to know when AI has
        # completely finished speaking.
        self.response_finished = (
            asyncio.Event()
        )

        # We are initially ready to listen.
        self.response_finished.set()

        print(
            "✅ Kokoro TTS processor ready"
        )

    async def process_frame(
        self,
        frame,
        direction: FrameDirection,
    ):
        await super().process_frame(
            frame,
            direction,
        )

        if isinstance(
            frame,
            LLMFullResponseStartFrame,
        ):

            self.response_text = ""

            self.response_finished.clear()

        elif isinstance(
            frame,
            LLMTextFrame,
        ):

            if frame.text:
                self.response_text += frame.text

        elif isinstance(
            frame,
            LLMFullResponseEndFrame,
        ):

            text = self.response_text.strip()

            if text:

                print(
                    f"\n🔊 Speaking..."
                )

                # Kokoro is synchronous, so run it
                # outside the Pipecat event loop.
                await asyncio.to_thread(
                    self.tts.speak,
                    text,
                )

            self.response_text = ""

            self.response_finished.set()

        await self.push_frame(
            frame,
            direction,
        )