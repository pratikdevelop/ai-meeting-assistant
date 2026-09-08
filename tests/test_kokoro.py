from chatbot.tts import KokoroTTS

def main():

    print("Starting Kokoro test...")

    tts = KokoroTTS()

    tts.speak(
        "Hello Pratik. Kokoro is now working as a local text to speech engine."
    )

    print("✅ Speech completed")


if __name__ == "__main__":
    main()