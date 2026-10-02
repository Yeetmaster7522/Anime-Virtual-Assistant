import ollama

with open("private/system_prompt.txt", "r") as f:
    content = f.read()
    print(content)

ollama.create(
    model="astra-q-uncensored", 
    from_="fredrezones55/Qwen3.5-Uncensored-HauhauCS-Aggressive:4b", 
    system=content
)

print("script completed successfully")