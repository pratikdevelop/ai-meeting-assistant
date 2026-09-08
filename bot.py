import os

from dotenv import load_dotenv
from loguru import logger

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.worker import (
    PipelineParams,
    PipelineWorker,
)
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.groq.llm import GroqLLMService
from pipecat.services.groq.stt import GroqSTTService
from pipecat.transports.base_transport import (
    BaseTransport,
    TransportParams,
)
from pipecat.workers.runner import WorkerRunner

from chatbot.kokoro_service import KokoroTTSService
from config.settings import settings


load_dotenv(override=True)


transport_params = {
    "webrtc": lambda: TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
    ),
}


async def run_bot(
    transport: BaseTransport,
    runner_args: RunnerArguments,
):
    logger.info("Starting Pipecat browser voice assistant")

    # ----------------------------
    # Speech-to-Text
    # ----------------------------
    stt = GroqSTTService(
        api_key=settings.groq_api_key,
        settings=GroqSTTService.Settings(
            model=settings.whisper_model,
            language="en",
        ),
    )

    # ----------------------------
    # LLM
    # ----------------------------
    llm = GroqLLMService(
        api_key=settings.groq_api_key,
        settings=GroqLLMService.Settings(
            model=settings.model,
            system_instruction=(
                "You are a helpful voice assistant. "
                "Speak naturally and concisely. "
                "Do not use markdown, bullets, emojis, "
                "or unnecessary formatting."
            ),
        ),
    )

    # ----------------------------
    # Kokoro TTS
    # ----------------------------
    tts = KokoroTTSService(
        voice="af_heart",
        speed=1.0,
        sample_rate=24000,
    )

    # ----------------------------
    # Context
    # ----------------------------
    context = LLMContext(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful voice assistant. "
                    "Answer naturally and concisely."
                ),
            }
        ]
    )

    # ----------------------------
    # Aggregators + VAD
    # ----------------------------
    user_aggregator, assistant_aggregator = (
        LLMContextAggregatorPair(
            context,
            user_params=LLMUserAggregatorParams(
                vad_analyzer=SileroVADAnalyzer()
            ),
        )
    )

    # ----------------------------
    # Pipeline
    # ----------------------------
    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            user_aggregator,
            llm,
            tts,
            transport.output(),
            assistant_aggregator,
        ]
    )

    # ----------------------------
    # Worker
    # ----------------------------
    worker = PipelineWorker(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
        idle_timeout_secs=(
            runner_args.pipeline_idle_timeout_secs
        ),
    )

    # ----------------------------
    # Runner
    # ----------------------------
    runner = WorkerRunner(
        handle_sigint=runner_args.handle_sigint
    )

    await runner.add_workers(worker)

    @transport.event_handler("on_client_connected")
    async def on_client_connected(
        transport,
        client,
    ):
        logger.info(
            "Browser client connected"
        )

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(
        transport,
        client,
    ):
        logger.info(
            "Browser client disconnected"
        )

        await runner.cancel()

    await runner.run()


async def bot(
    runner_args: RunnerArguments,
):
    """
    Pipecat runner entry point.
    """

    transport = await create_transport(
        runner_args,
        transport_params,
    )

    await run_bot(
        transport,
        runner_args,
    )


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()