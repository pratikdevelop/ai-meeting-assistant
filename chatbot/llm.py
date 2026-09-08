from pipecat.services.groq.llm import GroqLLMService

from config.settings import settings


def create_llm() -> GroqLLMService:

    return GroqLLMService(
        api_key=settings.groq_api_key,
        settings=GroqLLMService.Settings(
            model=settings.model,
            system_instruction=(
                "You are a helpful voice assistant. "
                "Respond clearly, naturally, and briefly. "
                "Your answers will be spoken aloud. "
                "Do not use markdown, bullet points, emojis, "
                "or formatting that sounds unnatural when spoken."
            ),
        ),
    )