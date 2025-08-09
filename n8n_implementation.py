import requests

with open("appointment_instructions.txt") as f:
    instructions = f.read()

payload = {"instructions": instructions}
res = requests.post("http://localhost:5678/webhook/abcd1234", json=payload)
print(res.status_code, res.text)
