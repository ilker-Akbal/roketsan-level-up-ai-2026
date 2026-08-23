import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    print("API key is not found")
    
model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)

prompt = ChatPromptTemplate(
    [
        ("system","Sen teknik konuları anlatan bir eğitim asistanısın"),
        ("human","""{topic}""")
    ]
)

messages =prompt.format_messages(topic="Büyük dil modelleri hakkında bilgi ver")

response = model.invoke(messages)

print(response.content)