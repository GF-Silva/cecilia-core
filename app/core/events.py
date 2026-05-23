from asyncio import Event

stt_started = Event()
stt_stopped = Event()
llm_running = Event()
llm_responding = Event()
tts_running = Event()