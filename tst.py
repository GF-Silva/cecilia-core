from groq import Groq

client = Groq(api_key="***REMOVIDO***")

def multi_turn_conversation():
    # Initial conversation with system message and first user input
    initial_messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant that provides detailed explanations about complex topics. Always provide comprehensive answers with examples and context."
        },
        {
            "role": "user",
            "content": "What is quantum computing?"
        }
    ]
    

    # First request - creates cache for system message
    first_response = client.chat.completions.create(
        messages=initial_messages, # pyright: ignore[reportArgumentType]
        model="openai/gpt-oss-120b"
    )

    # Continue conversation - system message and previous context will be cached
    conversation_messages = [ # pyright: ignore[reportUnknownVariableType]
        *initial_messages,
        first_response.choices[0].message,
        {
            "role": "user",
            "content": "Can you give me a simple example of how quantum superposition works?"
        }
    ]

    second_response = client.chat.completions.create(
        messages=conversation_messages, # pyright: ignore[reportUnknownArgumentType]
        model="openai/gpt-oss-120b"
    )

    # Continue with third turn
    third_turn_messages = [ # pyright: ignore[reportUnknownVariableType]
        *conversation_messages,
        second_response.choices[0].message,
        {
            "role": "user",
            "content": "How does this relate to quantum entanglement?"
        }
    ]

    third_response = client.chat.completions.create(
        messages=third_turn_messages, # pyright: ignore[reportUnknownArgumentType]
        model="openai/gpt-oss-120b"
    )

    print("Third response:", third_response.choices[0].message.content)
    print("Usage:", third_response.usage)

if __name__ == "__main__":
    multi_turn_conversation()