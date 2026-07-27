from dotenv import load_dotenv

load_dotenv()
from langchain.chat_models import init_chat_model

init_chat_model()

model = init_chat_model(
    "gemini-3.5-flash",
    model_provider="google_genai"
)

print(model)