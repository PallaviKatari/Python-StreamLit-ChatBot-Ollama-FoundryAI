import os
import asyncio
import base64
import queue
from dotenv import load_dotenv
import sounddevice as sd
from azure.identity.aio import AzureCliCredential
from azure.ai.voicelive.aio import connect
from azure.ai.voicelive.models import (
    InputAudioFormat,
    Modality,
    OutputAudioFormat,
    RequestSession,
    ServerEventType,
    AudioNoiseReduction,
    AudioEchoCancellation,
    AzureSemanticVadMultilingual,
    AgentConfig,
)


def main():
    """Main entry point."""
    try:
        os.system("cls" if os.name == "nt" else "clear")
        load_dotenv()

        endpoint = os.environ.get("FOUNDRY_ENDPOINT")
        agent_name = os.environ.get("AZURE_VOICELIVE_AGENT_ID")
        project_name = os.environ.get("AZURE_VOICELIVE_PROJECT_NAME")

        agent_config = AgentConfig(
            {
                "agent_name": agent_name,
                "project_name": project_name,
            }
        )

        credential = AzureCliCredential()

        assistant = VoiceAssistant(
            endpoint=endpoint,
            credential=credential,
            agent_config=agent_config,
        )

        try:
            asyncio.run(assistant.start())
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

    except Exception as e:
        print(f"Startup error: {e}")


class VoiceAssistant:
    """ Main voice assistant that coordinates the conversation flow. """

    def __init__(self, endpoint, credential, agent_config):
        self.endpoint = endpoint
        self.credential = credential
        self.agent_config = agent_config

    async def start(self):
        print("\n" + "=" * 60)
        print("🎙️ AZURE VOICELIVE VOICE AGENT")
        print("=" * 60)
        try:
            async with connect(
                endpoint=self.endpoint,
                credential=self.credential,
                api_version="2026-01-01-preview",
                agent_config=self.agent_config,
            ) as connection:
                self.connection = connection

                self.audio_processor = AudioProcessor(connection)

                await self.setup_session()
                self.audio_processor.start_playback()

                print("\n✅ Ready! Start speaking...")
                print("Press Ctrl+C to exit\n")

                await self.process_events()

        finally:
            if hasattr(self, "audio_processor"):
                self.audio_processor.shutdown()

    async def setup_session(self):
        session_config = RequestSession(
            model=os.environ.get["AZURE_OPENAI_DEPLOYMENT"],
            modalities=[Modality.TEXT, Modality.AUDIO],
            input_audio_format=InputAudioFormat.PCM16,
            output_audio_format=OutputAudioFormat.PCM16,
            turn_detection=AzureSemanticVadMultilingual(),
            input_audio_echo_cancellation=AudioEchoCancellation(),
            input_audio_noise_reduction=AudioNoiseReduction(
                type="azure_deep_noise_suppression"
            ),
        )
        await self.connection.session.update(session=session_config)
        print("⚙️ Session configured")

    async def process_events(self):
        async for event in self.connection:
            await self.handle_event(event)

    async def handle_event(self, event):
        if event.type == ServerEventType.SESSION_UPDATED:
            print(f"📡 Connected to agent: {event.session.agent.name}")
            self.audio_processor.start_capture()

        elif event.type == ServerEventType.CONVERSATION_ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
            print(f'👤 You: {event.get("transcript", "")}')

        elif event.type == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
            print(f'🤖 Agent: {event.get("transcript", "")}')

        elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
            self.audio_processor.clear_playback_queue()
            print("🎤 Listening...")

        elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED:
            print("🤔 Thinking...")

        elif event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
            self.audio_processor.queue_audio(event.delta)

        elif event.type == ServerEventType.RESPONSE_AUDIO_DONE:
            print("✓ Response complete\n")

        elif event.type == ServerEventType.ERROR:
            print(f"❌ Error: {event.error.message}")


class AudioProcessor:
    """ Handles microphone input and speaker output using sounddevice. """

    def __init__(self, connection):
        self.connection = connection
        self.sample_rate = 24000
        self.channels = 1
        self.block_size = 1200
        self.input_stream = None
        self.output_stream = None
        self.playback_queue = queue.Queue()
        self.loop = None
        self.running = False

    def start_capture(self):
        self.loop = asyncio.get_running_loop()
        self.running = True

        def input_callback(indata, frames, time_info, status):
            if status:
                print(f"Input Status: {status}")
            if not self.running or self.connection.is_closed:
                return
            try:
                audio_bytes = bytes(indata)
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
                asyncio.run_coroutine_threadsafe(
                    self.safe_append(audio_base64), self.loop
                )
            except Exception as ex:
                print(f"Capture error: {ex}")

        self.input_stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=self.block_size,
            callback=input_callback,
        )
        self.input_stream.start()
        print("🎤 Microphone started")

    async def safe_append(self, audio_base64):
        if self.connection.is_closed or not self.running:
            return
        try:
            await self.connection.input_audio_buffer.append(audio=audio_base64)
        except RuntimeError:
            print("⚠️ Transport closed, skipping audio append")

    def start_playback(self):
        def output_callback(outdata, frames, time_info, status):
            if status:
                print(f"Output Status: {status}")
            try:
                audio_data = self.playback_queue.get_nowait()
                if audio_data is None:
                    outdata[:] = bytes(len(outdata))
                    return
                required = len(outdata)
                if len(audio_data) < required:
                    audio_data += bytes(required - len(audio_data))
                outdata[:] = audio_data[:required]
            except queue.Empty:
                outdata[:] = bytes(len(outdata))

        self.output_stream = sd.RawOutputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=self.block_size,
            callback=output_callback,
        )
        self.output_stream.start()
        print("🔊 Speakers ready")

    def queue_audio(self, audio_data):
        try:
            if isinstance(audio_data, str):
                audio_data = base64.b64decode(audio_data)
            self.playback_queue.put(audio_data)
        except Exception as ex:
            print(f"Playback error: {ex}")

    def clear_playback_queue(self):
        while not self.playback_queue.empty():
            try:
                self.playback_queue.get_nowait()
            except queue.Empty:
                break

    def shutdown(self):
        self.running = False
        try:
            if self.input_stream:
                self.input_stream.stop()
                self.input_stream.close()
            if self.output_stream:
                self.output_stream.stop()
                self.output_stream.close()
        except Exception as ex:
            print(f"Shutdown error: {ex}")
        print("🔇 Audio stopped")


if __name__ == "__main__":
    main()
