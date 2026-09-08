from collections import deque
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf
import webrtcvad
from openai import OpenAI

from config.settings import settings


class WhisperService:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        self.sample_rate = settings.audio_sample_rate
        self.channels = 1

        # WebRTC VAD works with 10, 20, or 30 ms frames.
        self.frame_duration_ms = 30

        self.frame_size = int(
            self.sample_rate
            * self.frame_duration_ms
            / 1000
        )

        self.vad = webrtcvad.Vad(
            settings.vad_mode
        )

        self.silence_frames = max(
            1,
            int(
                settings.vad_silence_ms
                / self.frame_duration_ms
            ),
        )

        self.start_timeout_frames = max(
            1,
            int(
                settings.vad_start_timeout_ms
                / self.frame_duration_ms
            ),
        )

        self.max_frames = max(
            1,
            int(
                settings.max_recording_seconds
                * 1000
                / self.frame_duration_ms
            ),
        )

    def record(
        self,
        filename: str = "recording.wav",
    ):
        """
        Record one speech turn using WebRTC VAD.

        Recording starts when speech is detected and ends
        after a period of silence.
        """

        print("\n🎤 Listening...")

        recorded_frames = []

        # Keep a small pre-roll so we don't clip the
        # beginning of the first word.
        pre_roll = deque(maxlen=10)

        speech_started = False
        silent_count = 0
        total_frames = 0

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="int16",
                blocksize=self.frame_size,
            ) as stream:

                while total_frames < self.max_frames:

                    audio, overflowed = stream.read(
                        self.frame_size
                    )

                    if overflowed:
                        print(
                            "⚠️ Audio buffer overflow detected."
                        )

                    audio = np.asarray(
                        audio,
                        dtype=np.int16,
                    )

                    frame_bytes = audio.tobytes()

                    is_speech = self.vad.is_speech(
                        frame_bytes,
                        self.sample_rate,
                    )

                    total_frames += 1

                    if not speech_started:

                        pre_roll.append(audio.copy())

                        if is_speech:

                            speech_started = True

                            print(
                                "🗣️ Speech detected..."
                            )

                            recorded_frames.extend(
                                list(pre_roll)
                            )

                            pre_roll.clear()

                        elif (
                            total_frames
                            >= self.start_timeout_frames
                        ):
                            print(
                                "⏱️ No speech detected."
                            )
                            return None

                    else:

                        recorded_frames.append(
                            audio.copy()
                        )

                        if is_speech:
                            silent_count = 0

                        else:
                            silent_count += 1

                        if (
                            silent_count
                            >= self.silence_frames
                        ):
                            print(
                                "🛑 Speech ended."
                            )
                            break

        except KeyboardInterrupt:
            print("\n🛑 Recording interrupted.")
            sd.stop()
            return None

        if not recorded_frames:
            return None

        recording = np.concatenate(
            recorded_frames,
            axis=0,
        )

        output_path = Path(filename)

        sf.write(
            output_path,
            recording,
            self.sample_rate,
            subtype="PCM_16",
        )

        print(
            f"✅ Saved recording to {output_path}"
        )

        return str(output_path)

    def transcribe(self, filename: str):

        if not filename:
            return ""

        print(
            "🧠 Sending audio to Groq Whisper..."
        )

        with open(filename, "rb") as audio:

            result = (
                self.client.audio.transcriptions.create(
                    model=settings.whisper_model,
                    file=audio,
                    language="en",
                )
            )

        text = result.text.strip()

        return text