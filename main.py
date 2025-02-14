import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor


class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")


client = Groq(
    api_key=os.environ.get('GROQ_API_KEY'),
)

client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

def ask_question(question):
    resp = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        response_model=Character,
    )
    return resp.model_dump_json(indent=2)

def main():
    print("You can now ask questions to the Groq API. Type 'quit' to exit.")
    while True:
        question = input("Ask a question: ")
        if question.lower() == "quit":
            print("Exiting the loop. Goodbye!")
            break
        response = ask_question(question)
        print(response)

if __name__ == "__main__":
    main()
    