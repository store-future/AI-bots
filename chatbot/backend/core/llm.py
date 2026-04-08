import requests

class LLMClient:
    
    def __init__(self,model,url):
        self.model = model
        self.url = url

    def generate(self,prompt):
        payload = {
            "model": self.model,
            "input": prompt
        }

        res = requests.post(self.url, json=payload)

        if res.status_code == 200:
            return res.json()['output'][0]['content']

        return "error"