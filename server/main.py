# Set ollama api key to access web search and fetch tools
import os

with open("private/apikey.txt", "r") as f:
    key = f.read()

os.environ["OLLAMA_API_KEY"] = key
print(os.getenv("OLLAMA_API_KEY"))


from chat import LM
from tts import TTS
from threading import Thread
from queue import Queue
import tools
from ollama import web_search, web_fetch


# setup language model and text-to-speech
lm = LM(
    model="astra-q", 
    tools={
        "web_search": tools.web_search, 
        "web_fetch": tools.get_website_content,
        "get_datetime": tools.get_datetime,
        "take_screenshot": tools.take_screenshot,
        "run_command": tools.run_command,
        "backup_search": web_search,
        "backup_fetch": web_fetch,
    }
)
tts = TTS(rate=200, voice_index=2)


def main(queue: Queue):
    """
    KEY PARAMETERS:
        queue: the sound queue

    Gets user input and passes it onto LLM as well as flushing the voice queue.
    When user types /break it will stop the process.
    """
    
    while True:
        # get message
        msg = input("\n\n-> ")
        if msg == "/break": break

        # flush voice queue
        while not queue.empty():
            queue.get_nowait()
            queue.task_done()

        lm.talk(msg, queue)
        
    # kill model
    lm.stop()

# multithreading
q = Queue()
t1 = Thread(target=main, args=(q, ))
t2 = Thread(target=tts.worker, args=(q, ), daemon=True)
t1.start()
t2.start()

t1.join()
q.join()