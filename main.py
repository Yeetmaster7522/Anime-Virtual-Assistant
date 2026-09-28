import os

with open("apikey.txt", "r") as f:
    key = f.read()
os.environ["OLLAMA_API_KEY"] = key
print(os.getenv("OLLAMA_API_KEY"))


from chat import LM


lm = LM(model="astra-q")

while True:
    msg = input("\n\n-> ")
    if msg == "/break": break

    lm.talk(msg)

# kill model
lm.stop()