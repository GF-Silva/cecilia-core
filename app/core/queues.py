from asyncio import Queue

transcription_queue: Queue[str] = Queue()
llm_stream_queue: Queue[str] = Queue()