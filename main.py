from ollama import chat

messages = []

while True:
    msg = input("\n\n-> ")
    if msg == "/break": break
    
    messages.append({ "role": "user", "content": msg })
    
    # get response from model
    stream = chat(
        model="astra",
        messages=messages,
        stream=True,
    )

    # stream response
    content = ""
    for chunk in stream:
        print(chunk.message.content, end="", flush=True)
        content += chunk.message.content

    # append accumulated fields to the messages for the next request
    messages.append({ "role": "assistant", "content": content })

    # print(f"\n\n{messages}") # debug