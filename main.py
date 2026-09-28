import os

with open("apikey.txt", "r") as f:
    key = f.read()
os.environ["OLLAMA_API_KEY"] = key
print(os.getenv("OLLAMA_API_KEY"))

from ollama import chat, web_search, web_fetch
from subprocess import run

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
        tools=[web_search, web_fetch],
        keep_alive="30m",
    )

    # stream response
    content = ""
    tool_calls = []
    
    for chunk in stream:
        print(chunk.message.content, end="", flush=True)
        content += chunk.message.content

        if chunk.message.tool_calls:
            tool_calls.extend(chunk.message.tool_calls)
            print(chunk.message.tool_calls)

    # append accumulated fields to the messages for the next request
    if content or tool_calls:
        messages.append({ "role": "assistant", "content": content, "tool_calls": tool_calls })

    for call in tool_calls:
        try:
            fn = available_tools[call.function.name]
            result = fn(**call.function.arguments)
            messages.append({ "role": "tool", "tool_name": call.function.name, "content": str(result) })
        except Exception as e:
            print(e)


    if tool_calls:
        followup_stream = chat(
            model=model,
            messages=messages,
            stream=True,
            think=False,
            keep_alive="30m",
        )

        final_content = ""
        for chunk in followup_stream:
            print(chunk.message.content, end="", flush=True)
            final_content += chunk.message.content

        messages.append({
            "role": "assistant",
            "content": final_content
        })

    # print(f"\n\n{messages}")



# kill model
run(["ollama", "stop", model])
print("Model stopped succesfully")