from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model

# model = init_chat_model("gemini-2.5-flash",model_provider="google_genai")

# response = model.invoke("Who is virat kohli and why he is famous")
# print(response.content)

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

answer = model.invoke("do you know who is shahrukh khan?")
print(answer.content)