from pipecat.processors.frame_processor import (
    FrameProcessor,
    FrameDirection,
)


class DebugProcessor(FrameProcessor):

    def __init__(self, label):
        super().__init__()
        self.label = label

    async def process_frame(self, frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        print(f"[{self.label}] {type(frame).__name__}")

        await self.push_frame(frame, direction)