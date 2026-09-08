import asyncio
from pipecat.frames.frames import LLMMessagesAppendFrame
from pipecat.processors.frame_processor import (
    FrameProcessor,
    FrameDirection,
)
from pipecat.frames.frames import (
    StartFrame,
    CancelFrame,
)



class ConsoleInputProcessor(FrameProcessor):
    """
    Reads user input from the terminal and injects it into the pipeline.
    """

    async def process_frame(self, frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, StartFrame):
            await self.push_frame(frame, direction)

            # Start the keyboard loop in the background
            asyncio.create_task(self._input_loop())

            return

        if isinstance(frame, CancelFrame):
            await self.push_frame(frame, direction)
            return

        await self.push_frame(frame, direction)

    async def _input_loop(self):

        while True:

            user_input = await asyncio.to_thread(input, "\nYou: ")


            if user_input.lower() in ("exit", "quit"):
                await self.push_frame(CancelFrame())
                break

            await self.push_frame(
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