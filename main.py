from ollama import chat, web_search, web_fetch
import subprocess

available_tools = {"web_search": web_search, "web_fetch": web_fetch}
model = "astra-q"

messages = []

while True:
    msg = input("\n\n-> ")
    if msg == "/break": break

    messages.append({ "role": "user", "content": msg })
    # messages.append({ "role": "user", "content": msg, "images": ["screenie.png"] })
    
    # get response from model
    stream = chat(
        model=model,
        messages=messages,
        stream=True,
        think=False,
        # tools=[web_search, web_fetch],
        keep_alive="30m",
    )

    # stream response
    content = ""
    for chunk in stream:
        print(chunk.message.content, end="", flush=True)
        content += chunk.message.content

    # append accumulated fields to the messages for the next request
    messages.append({ "role": "assistant", "content": content })

    # print(f"\n\n{messages}")



# kill model
subprocess.run(["ollama", "stop", model])
print("Model stopped succesfully")