import requests

url = "https://open-ai-text-to-speech1.p.rapidapi.com/"

payload = {
	"model": "tts-1",
	"input": "Today is a wonderful day",
	"voice": "alloy"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "5147683f9cmshf6827deecef7e05p1639c6jsn1dc628b85913",
	"X-RapidAPI-Host": "open-ai-text-to-speech1.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())