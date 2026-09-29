import pyttsx3
from queue import Queue

class TTS:
    def __init__(self, rate=150, volume=1.0, id=0):
        self.__rate = rate
        self.__volume = volume
        self.__id = id

    def speak(self, txt):
        try:
            self.__engine = pyttsx3.init()
            self.__engine.setProperty("rate", self.__rate)
            self.__engine.setProperty("volume", self.__volume)

            voices = self.__engine.getProperty("voices")
            self.__engine.setProperty("voice", voices[self.__id].id)
            
            self.__engine.say(txt)
            self.__engine.runAndWait()
            self.__engine.stop()
        except Exception as e:
            print(e)

    def worker(self, queue: Queue):
        buffer = ""

        while True:
            chunk = queue.get()
            buffer += chunk
            # print(buffer)

            if buffer.endswith((".", "!", "?", "\n", "]", ",", ":", "。", "？", "～", "、")):
                self.speak(buffer)
                buffer = ""
            queue.task_done()