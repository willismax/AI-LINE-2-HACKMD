import openai
import os
# from config import OPENAI_API_KEY

openai.api_key = os.environ.get("OPENAI_API_KEY")
chat_language = "zh" 
MSG_LIST_LIMIT = 20
LANGUAGE_TABLE = {
	  "zh": "哈囉！",
	  "en": "Hello!"
	}
class Prompt:
    def __init__(self):
        self.msg_list = []
        self.msg_list.append(f"AI:{LANGUAGE_TABLE[chat_language]}")
	    
    def add_msg(self, new_msg):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.remove_msg()
        self.msg_list.append(new_msg)

    def remove_msg(self):
        self.msg_list.pop(0)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)	
	
class OpenAIBot:
    def __init__(self):
        self.prompt = Prompt()
        self.model = "gpt-3.5-turbo" #os.getenv("OPENAI_MODEL", default = "text-davinci-003")
        self.temperature = 0.9 #float(os.getenv("OPENAI_TEMPERATURE", default = 0))
        self.frequency_penalty = 0 #float(os.getenv("OPENAI_FREQUENCY_PENALTY", default = 0))
        self.presence_penalty = 0.6 #float(os.getenv("OPENAI_PRESENCE_PENALTY", default = 0.6))
        self.max_tokens = 240 #int(os.getenv("OPENAI_MAX_TOKENS", default = 240))
	
    def get_response(self):
        response = openai.ChatCompletion.create(
	            model=self.model,
	            prompt=self.prompt.generate_prompt(),
	            temperature=self.temperature,
	            frequency_penalty=self.frequency_penalty,
	            presence_penalty=self.presence_penalty,
	            max_tokens=self.max_tokens
	        )
        print(response['choices'][0]['text'].strip())
        print(response)
        return response['choices'][0]['text'].strip()
	
    def add_msg(self, text):
        self.prompt.add_msg(text)

    
    
