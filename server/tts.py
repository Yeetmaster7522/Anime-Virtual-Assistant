import pyttsx3
from queue import Queue

class TTS:
    """
    Turns txt into speech

    Functions:
        worker: Runs in a loop. Checks sound queue for sound requests and fulfills them.
    """
    
    def __init__(self, rate=150, volume=1.0, voice_index=0):
        """
        KEY PARAMETERS
            rate: rate of speech / how fast it talks
            volume: from 0 to 1. Controls volume of speech
            voice_index: allows for selection of voice from engine.getProperty("voices")
        """
        
        self.__rate = rate
        self.__volume = volume
        self.voice_index = voice_index

    def __speak(self, txt: str):
        """
        KEY PARAMETERS:
            txt: the txt that will be turned into speech

        Converts txt into speech.
        
        Because of some technical issues the approach used here is most likely inefficient.
        """

        # sets property of voice engine
        self.__engine = pyttsx3.init()
        self.__engine.setProperty("rate", self.__rate)
        self.__engine.setProperty("volume", self.__volume)

        voices = self.__engine.getProperty("voices")
        self.__engine.setProperty("voice", voices[self.voice_index].id)

        # says txt aloud and allows it to finish
        self.__engine.say(txt)
        self.__engine.runAndWait()
        self.__engine.stop()
        
    def worker(self, queue: Queue):
        """
        KEY PARAMETERS
            queue: the sound queue

        Fulfills all requests in sound queue. This should be a daemon thread.

        Instead of doing single tokens it waits until it accumulates a sentence or so before turning it into speech.
        """
        
        buffer = ""

        while True:
            # adds new chunks to buffer
            chunk = queue.get()
            buffer += chunk

            # if the buffer has accumulated a sentence or half a sentence it will speak it and reset the buffer
            if buffer.endswith((".", "!", "?", "\n", "]", ",", ":", "。", "？", "～", "、")):
                self.__speak(buffer)
                buffer = ""
            queue.task_done()