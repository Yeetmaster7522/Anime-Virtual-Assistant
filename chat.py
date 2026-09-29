from ollama import chat, web_search, web_fetch
from subprocess import run

class LM:
    def __init__(
            self, 
            model, 
            tools={"web_search": web_search, "web_fetch": web_fetch}, 
            stream=True, 
            think=False, 
            keep_alive="30m"
            ):
        self.__messages = []

        self.__model = model

        self.__tools = tools
        self.__stream = stream
        self.__think = think
        self.__keep_alive = keep_alive

    def talk(self, msg, queue, role="user"):
        if msg != "": self.__messages.append({ "role": role, "content": msg })

        content, tool_calls = self.stream(queue)

        # append accumulated fields to the messages for the next request
        if content or tool_calls:
            self.__messages.append({ "role": "assistant", "content": content, "tool_calls": tool_calls })

        for call in tool_calls:
            try:
                fn = self.__tools[call.function.name]
                result = fn(**call.function.arguments)
                self.__messages.append({ "role": "tool", "tool_name": call.function.name, "content": str(result) })
            except Exception as e:
                print(e)

        if tool_calls: self.talk("", queue)

    def stream(self, queue):
        # get response from model
        stream = chat(
            model=self.__model,
            messages=self.__messages,
            stream=self.__stream,
            think=self.__think,
            tools=self.__tools.values(),
            keep_alive=self.__keep_alive,
        )

        # stream response
        content = ""
        tool_calls = []

        for chunk in stream:
            print(chunk.message.content, end="", flush=True)
            queue.put(chunk.message.content)
            content += chunk.message.content

            if chunk.message.tool_calls:
                print(chunk.message.tool_calls)
                tool_calls.extend(chunk.message.tool_calls)

        return content, tool_calls

    def stop(self):
        # kill model
        run(["ollama", "stop", self.__model])
        print("Model stopped succesfully")