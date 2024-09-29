from groq import Groq
from dotenv import load_dotenv
import os


class LLM:
    def __init__(self, model_name, api_key) -> None:
        self.client = Groq(
            api_key=api_key
        )
        self.model_name = model_name
        self.sys_prompt = """
            You are a helpful summary generator. I will provide data in a pandas dataframe format, and your task is to generate a concise summary for each author using their attributes. The summary format should be as follows:
            ```
            <author-name>
            Expertise: <author-expertise>
            Interests: <author-interest>

            Author publications:
            <author-paper-title>
            <a-short-summary-of-the-paper-by-considering-the-attributes-provided>
            ```
            Please use clear and informative language when summarizing each paper, ensuring that the summary highlights key aspects based on the author's expertise and interests.
        """
    
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
