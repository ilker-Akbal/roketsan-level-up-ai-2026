from ollama import chat


LLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"


# =========================================================
# CONVERSATION MEMORY
# =========================================================

chat_history = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant. "
            "Answer in the same language as the user."
        )
    }
]


def ask(message):

    # User mesajını memory'ye ekle
    chat_history.append(
        {
            "role": "user",
            "content": message
        }
    )


    # Bütün geçmişi tekrar LLM'e gönder
    response = chat(
        model=LLM_MODEL,
        messages=chat_history,
        options={
            "temperature": 0.1
        }
    )


    answer = response.message.content


    # Assistant cevabını da memory'ye ekle
    chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    return answer


# =========================================================
# TEST
# =========================================================

answer1 = ask(
    "Benim aracım F-16. Bunu konuşmamız boyunca hatırla."
)

print("\nUSER:")
print("Benim aracım F-16. Bunu konuşmamız boyunca hatırla.")

print("\nASSISTANT:")
print(answer1)


answer2 = ask(
    "Benim aracım neydi?"
)

print("\nUSER:")
print("Benim aracım neydi?")

print("\nASSISTANT:")
print(answer2)