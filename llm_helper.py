from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(groq_api_key=os.getenv("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"), model_name="llama-3.3-70b-versatile")


if __name__ == "__main__":
    response = llm.invoke("Two most important ingradient in samosa are ")
    print(response.content)
