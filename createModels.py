import ollama

with open("private/system_prompt.txt", "r") as f:
    content = f.read()
    print(content)

ollama.create(
    model="astra-q", 
    from_="qwen3.5:0.8b", 
    system=content
)

print("script completed successfully")