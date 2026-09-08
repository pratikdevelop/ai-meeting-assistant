import asyncio

from chatbot.runner import ChatbotRunner


async def main():
    bot = ChatbotRunner()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())