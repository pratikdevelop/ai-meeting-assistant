from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.task import PipelineTask

from chatbot.context import create_context
from chatbot.llm import create_llm
from chatbot.aggregator import create_aggregators

from processors.console_output import (
    ConsoleOutputProcessor,
)

from processors.kokoro_tts import (
    KokoroTTSProcessor,
)


class ChatPipeline:

    def __init__(self):

        # Context
        self.context = create_context()

        # LLM
        self.llm = create_llm()

        # Aggregators
        self.user_agg, self.assistant_agg = (
            create_aggregators(
                self.context
            )
        )

        # Console output
        self.console_output = (
            ConsoleOutputProcessor()
        )

        # Kokoro TTS
        self.kokoro_tts = (
            KokoroTTSProcessor()
        )

        # Pipeline
        self.pipeline = Pipeline(
            [
                self.user_agg,
                self.llm,
                self.console_output,
                self.kokoro_tts,
                self.assistant_agg,
            ]
        )

        # Task
        self.task = PipelineTask(
            self.pipeline
        )