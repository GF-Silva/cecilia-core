from asyncio import Event

stt_started: Event = Event()
stt_stopped: Event = Event()
llm_running: Event = Event()
llm_responding: Event = Event()
tts_running: Event = Event()