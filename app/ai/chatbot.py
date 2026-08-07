import json
from datetime import datetime
from app.ai.prompts import get_prompt

class Chatbot:
    def __init__(self, client, mode, context):
        self.client = client
        self.mode = mode
        self.context = context
        self.conversation_history = [
            {
                "role": "system",
                "content": self._build_system_prompt()
            }
        ]


    def send_message(self, user_input):
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        stream = self.client.responses.create(
            model="gpt-4.1-mini",
            input=self.conversation_history,
            stream=True
        )

        ai_response = ""

        for event in stream:
            if event.type == "response.output_text.delta":
                ai_response += event.delta

        self.conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })

        return ai_response
    

    def save_chat(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chats/session_{self.mode}_{timestamp}.json"

        with open(filename, "w") as file:
            json.dump(self.conversation_history, file, indent=4)


    def get_response(self, prompt):
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": self._build_system_prompt()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.output_text


    def get_structured_response(self, prompt, schema):
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": self._build_system_prompt()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            text={
                "format": schema
            }
        )

        return json.loads(response.output_text)
    

    def _build_system_prompt(self):
        return get_prompt(self.mode)