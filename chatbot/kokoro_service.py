import asyncio
from collections.abc import AsyncGenerator

import numpy as np

from kokoro import KPipeline

from pipecat.frames.frames import Frame, TTSAudioRawFrame
from pipecat.services.tts_service import TTSService
from pipecat.utils.tracing.service_decorators import traced_tts


class KokoroTTSService(TTSService):
    """
    Local Kokoro TTS service for Pipecat.

    Converts LLM text into raw PCM audio frames that can be
    sent to a Pipecat transport such as SmallWebRTC.
    """

    def __init__(
        self,
        voice: str = "af_heart",
        speed: float = 1.0,
        sample_rate: int = 24000,
        **kwargs,
    ):
        super().__init__(
            sample_rate=sample_rate,
            push_start_frame=True,
            push_stop_frames=True,
            **kwargs,
        )

        self.voice = voice
        self.speed = speed
        self.kokoro_sample_rate = sample_rate

        print("🧠 Loading Kokoro TTS...")

        self.pipeline = KPipeline(
            lang_code="a",
            repo_id="hexgrad/Kokoro-82M",
        )

        print("✅ Kokoro TTS loaded")

    def _generate_audio(self, text: str) -> np.ndarray:
        """
        Run Kokoro synchronously.
        This function is executed in a background thread.
        """

        chunks = []

        generator = self.pipeline(
            text,
            voice=self.voice,
            speed=self.speed,
        )

        for _, _, audio in generator:

            if hasattr(audio, "detach"):
                audio = (
                    audio.detach()
                    .cpu()
                    .numpy()
                )
            else:
                audio = np.asarray(audio)

            chunks.append(audio)

        if not chunks:
            return np.array([], dtype=np.int16)

        audio = np.concatenate(chunks)

        # Convert floating-point audio [-1, 1] to PCM16.
        audio = np.clip(audio, -1.0, 1.0)

        audio = (
            audio * 32767
        ).astype(np.int16)

        return audio

    @traced_tts
    async def run_tts(
        self,
        text: str,
        context_id: str,
    ) -> AsyncGenerator[Frame, None]:

        if not text or not text.strip():
            return

        audio = await asyncio.to_thread(
            self._generate_audio,
            text,
        )

        if audio.size == 0:
            return

        # 20 ms audio chunks.
        chunk_samples = int(
            self.kokoro_sample_rate * 0.02
        )

        for start in range(
            0,
            len(audio),
            chunk_samples,
        ):

            chunk = audio[
                start:start + chunk_samples
            ]

            if len(chunk) == 0:
                continue

            yield TTSAudioRawFrame(
                audio=chunk.tobytes(),
                sample_rate=self.kokoro_sample_rate,
                num_channels=1,
                context_id=context_id,
            )