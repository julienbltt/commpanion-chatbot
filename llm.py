import requests
import json
from tts import talk
import re

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
session = requests.Session()

def get_lmstudio_response(prompt, model="aya-expanse-8b", temperature=0.7):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": True 
    }

    try:
        with session.post(LMSTUDIO_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            buffer = ""
            full_text = ""

            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    content = line[len("data: "):]
                    if content == "[DONE]":
                        break
                    try:
                        data = json.loads(content)
                        delta = data["choices"][0]["delta"]
                        if "content" in delta:
                            chunk = delta["content"]
                            buffer += chunk
                            full_text += chunk


                            # Improved regex: look for sentence-ending punctuation followed by a space or end of line
                            sentence_pattern = r'([A-Z][^.!?,;:]*[.!?,;:])(?=\s|$)'
                            matches = list(re.finditer(sentence_pattern, buffer))

                            last_end = 0
                            for match in matches:
                                sentence = match.group(1).strip()
                                if sentence:
                                    talk(sentence)
                                last_end = match.end()

                            # Keep only the remaining unfinished part
                            buffer = buffer[last_end:]

                    except json.JSONDecodeError:
                        continue

            # Speak any leftover text
            if buffer.strip():
                talk(buffer.strip())

            return full_text

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"