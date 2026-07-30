import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY missing — check your .env file")

model = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google_genai",
)

question = "what is football?"
response = model.invoke(question)
print(response.content)