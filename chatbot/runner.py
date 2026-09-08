import asyncio

from pipecat.frames.frames import (
    LLMMessagesAppendFrame,
)
from pipecat.pipeline.runner import PipelineRunner

from chatbot.pipeline import ChatPipeline
from processors.voice_input import (
    VoiceInputProcessor,
)


class ChatbotRunner:

    def __init__(self):

        self.chat = ChatPipeline()
        self.voice = VoiceInputProcessor()

    async def start(self):

        print("=" * 60)
        print("         Pipecat Voice Assistant")
        print("=" * 60)

        print(
            "\n🎤 Voice Assistant Started"
        )

        print(
            "Say 'exit', 'quit', or 'stop' to quit.\n"
        )

        runner = PipelineRunner()

        runner_task = asyncio.create_task(
            runner.run(self.chat.task)
        )

        try:

            while True:

                # Do not start recording while Kokoro
                # is speaking.
                await (
                    self.chat.kokoro_tts
                    .response_finished
                    .wait()
                )

                print(
                    "\n🎤 Ready for your voice..."
                )

                # Microphone + Whisper are blocking,
                # so run them outside the asyncio loop.
                user_input = await asyncio.to_thread(
                    self.voice.listen
                )

                if not user_input:
                    continue

                command = (
                    user_input
                    .strip()
                    .lower()
                )

                # Check exit BEFORE sending to the LLM.
                if command in (
                    "exit",
                    "quit",
                    "stop",
                ):
                    print(
                        "\n👋 Goodbye!"
                    )
                    break

                print(
                    "\n>>> Sending message to Pipecat..."
                )

                # Mark that we're now waiting for
                # a new AI response.
                self.chat.kokoro_tts.response_finished.clear()

                await self.chat.task.queue_frame(
                    LLMMessagesAppendFrame(
                        [
                            {
                                "role": "user",
                                "content": user_input,
                            }
                        ],
                        run_llm=True,
                    )
                )

                print(
                    ">>> Message queued."
                )

        except KeyboardInterrupt:

            print(
                "\n🛑 Keyboard interrupt received."
            )

        finally:

            print(
                "\nStopping chatbot..."
            )

            self.chat.kokoro_tts.tts.stop()

            await self.chat.task.cancel()

            try:
                await runner_task
            except asyncio.CancelledError:
                pass