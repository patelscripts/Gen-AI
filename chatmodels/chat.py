import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)

print(ai_msg.content)

# if not os.getenv("GOOGLE_API_KEY"):
#     raise RuntimeError("GOOGLE_API_KEY missing — check your .env file")

# model = init_chat_model(
#     "gemini-2.5-flash",
#     model_provider="google_genai",
# )

# question = "what is football?"
# response = model.invoke(question)
# print(response.content)