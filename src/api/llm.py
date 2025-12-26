from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def gerar_mensagem_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente profissional de cobrança bancária."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
