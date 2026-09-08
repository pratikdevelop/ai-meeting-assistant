from pipecat.frames.frames import (
    LLMFullResponseEndFrame,
    LLMFullResponseStartFrame,
    LLMTextFrame,
)

from pipecat.processors.frame_processor import (
    FrameDirection,
    FrameProcessor,
)


class ConsoleOutputProcessor(FrameProcessor):

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
            print("\nAI: ", end="", flush=True)

        elif isinstance(
            frame,
            LLMTextFrame,
        ):
            print(
                frame.text,
                end="",
                flush=True,
            )

        elif isinstance(
            frame,
            LLMFullResponseEndFrame,
        ):
            print()

        await self.push_frame(
            frame,
            direction,
        )