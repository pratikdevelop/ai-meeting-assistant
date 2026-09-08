from pipecat.frames.frames import LLMRunFrame


class ChatSession:

    def __init__(self, context, worker):
        self.context = context
        self.worker = worker

    async def start(self):
        print()

        while True:

            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye!")
                break

            self.context.add_message(
                {
                    "role": "user",
                    "content": user_input,
                }
            )

            await self.worker.queue_frames(
                [
                    LLMRunFrame()
                ]
            )