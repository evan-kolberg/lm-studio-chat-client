from openai import OpenAI
import requests
import json

try:
    # ./loophole.exe http 1234 --hostname llm
    address = "https://llm.loophole.site/"
    requests.get(address, timeout=5)
except requests.exceptions.Timeout:
    print(f"\033[31mCANNOT CONNECT TO REVERSE PROXY SERVER\033[37m")
    exit()

try:
    # if no model is currently loaded, the most recent will be used
    # if there are no models downloaded, i guess it just won't work
    model = json.loads(requests.get(address+"v1/models").text)["data"][0]["id"]
except:
    print(f"\033[32mREVERSE PROXY SERVER ONLINE\033[37m | \033[31mLLM SERVER OFFLINE\033[37m")
    exit()

client = OpenAI(base_url=address+"v1", api_key="lm-studio")
print(f'***\nCurrent Model: {model}')
print(f'Server: {address}')
print(f'\033[32mREVERSE PROXY SERVER ONLINE | LLM SERVER ONLINE\033[37m\n***\n')

history = [
    {"role": "system", "content": '''You are a knowledgeable, efficient, and direct AI assistant. Provide concise answers, focusing on the key information needed. Offer suggestions tactfully when appropriate to improve outcomes. Engage in productive collaboration with the user.'''},
    {"role": "user", "content": f'''{input("> ")}'''},
]

while True:
    completion = client.chat.completions.create(
        model=model,
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    print()
    history.append({"role": "user", "content": input("> ")})



