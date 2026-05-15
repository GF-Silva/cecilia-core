from groq import Groq
import threading

client = Groq(api_key="***REMOVIDO***")

stop_flag = threading.Event()

def listen_for_stop():
    input()  # espera o usuário apertar Enter
    stop_flag.set()

# roda o listener em paralelo
threading.Thread(target=listen_for_stop, daemon=True).start()

stream = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Count to 100."}
    ],
    model="llama-3.3-70b-versatile",
    stream=True
)

for chunk in stream:
    if stop_flag.is_set():
        print("\n[interrompido]")
        break
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)