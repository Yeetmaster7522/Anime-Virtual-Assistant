# from faster_whisper import WhisperModel

# model_size = "small.en"

# # Run on GPU with int8
# model = WhisperModel(model_size, device="cuda", compute_type="int8")

# segments, info = model.transcribe("private/Recording (9).m4a", language="en", beam_size=5)

# print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# for segment in segments:
#     print(segment.text)

import pyaudio
import wave

# Source - https://stackoverflow.com/q/40704026
# Posted by user4719989
# Retrieved 2026-09-29, License - CC BY-SA 3.0

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# https://atsss.medium.com/python-continuous-audio-recording-with-periodic-saving-3421735da820
# https://docs.cloud.google.com/speech-to-text/docs/v1/transcribe-streaming-audio?source=post_page-----3421735da820-----------------------------------------#speech-streaming-mic-recognize-python