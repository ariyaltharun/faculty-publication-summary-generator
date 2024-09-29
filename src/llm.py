from groq import Groq
from dotenv import load_dotenv
import os


class LLM: 
    def __init__(
        self, 
        model_name: str, 
        api_key: str, 
        sys_prompt: str="You are a helpful assistance"
    ) -> None:
        self.client = Groq(
            api_key=api_key
        )
        self.model_name = model_name
        self.sys_prompt = sys_prompt

    def __call__(self, user_prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.sys_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            model=self.model_name,
            temperature=0.1
        )
        response = chat_completion.choices[0].message.content
        # print(response)
        return response


if __name__ == "__main__":
    load_dotenv()
    llm = LLM("llama3-8b-8192", os.getenv("GROQ_API_KEY"))
    print(llm("Who are you?"))
