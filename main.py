import os

with open("apikey.txt", "r") as f:
    key = f.read()
os.environ["OLLAMA_API_KEY"] = key
print(os.getenv("OLLAMA_API_KEY"))


from chat import LM
from tts import TTS
from threading import Thread
from queue import Queue


lm = LM(model="astra-q")
tts = TTS(rate=200, id=2)

def main(queue: Queue):
    while True:
        msg = input("\n\n-> ")
        if msg == "/break": break

        while not queue.empty():
            queue.get_nowait()
            queue.task_done()

        lm.talk(msg, queue)
        
    # kill model
    lm.stop()

q = Queue()
t1 = Thread(target=main, args=(q, ))
t2 = Thread(target=tts.worker, args=(q, ), daemon=True)
t1.start()
t2.start()

q.join()