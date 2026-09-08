from pipecat.audio.vad.silero import SileroVADAnalyzer

from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)


def create_aggregators(context):

    user_aggregator, assistant_aggregator = (
        LLMContextAggregatorPair(
            context,
            user_params=LLMUserAggregatorParams(
                vad_analyzer=SileroVADAnalyzer()
            ),
        )
    )

    return (
        user_aggregator,
        assistant_aggregator,
    )