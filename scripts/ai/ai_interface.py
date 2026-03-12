import os
import requests


class AIInterface:

    def __init__(self):

        self.provider = os.getenv("AI_PROVIDER", "openai")
        self.api_key = os.getenv("AI_API_KEY")

    def generate(self, prompt):

        if self.provider == "openai":
            return self._openai(prompt)

        if self.provider == "local":
            return self._local_llm(prompt)

        raise Exception("unknown AI provider")

    def _openai(self, prompt):

        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        r = requests.post(url, json=payload, headers=headers)

        data = r.json()

        return data["choices"][0]["message"]["content"]

    def _local_llm(self, prompt):

        url = "http://localhost:11434/api/generate"

        payload = {
            "model": "llama3",
            "prompt": prompt
        }

        r = requests.post(url, json=payload)

        data = r.json()

        return data["response"]