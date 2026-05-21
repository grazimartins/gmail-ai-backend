import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class AIService:

    @staticmethod
    def summarize_email(email_body: str):

        prompt = f"""
        You are an AI assistant specialized in summarizing emails.

        Instructions:
        - Detect the language of the email automatically.
        - Write the summary ONLY in the same language as the email.
        - Do NOT mention the detected language.
        - Do NOT explain your reasoning.
        - Return only the final summary.

        The summary must be:
        - clear
        - objective
        - professional
        - concise

        EMAIL:
        {email_body}
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": (prompt)
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )

        return response.choices[0].message.content

    @staticmethod
    def generate_email_reply(email_body: str):
        
        prompt = f"""
        You are a professional AI email assistant.

        Instructions:
        - Detect the language of the email automatically.
        - Write the response ONLY in the same language as the email.
        - Do NOT mention the detected language.
        - Do NOT explain your reasoning.
        - Return ONLY the email response.

        The response must be:
        - polite
        - professional
        - objective
        - clear

        EMAIL:
        {email_body}
        """
                
        response = client.chat.completions.create(
            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": (prompt)
                },

                {
                    "role": "user",
                    "content": email_body
                }
            ],

            temperature=0.7
        )

        return response.choices[0].message.content