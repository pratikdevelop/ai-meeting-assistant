from pipecat.processors.aggregators.llm_context import LLMContext


SYSTEM_PROMPT = """
You are a helpful AI assistant.

Answer clearly and concisely.
Keep your responses friendly.
If you don't know something, say so honestly.
"""


def create_context() -> LLMContext:
    """
    Create the initial conversation context.
    """

    return LLMContext(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]
    )