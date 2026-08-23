import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from tools import general_question_tool, mil_std_rag_tool


load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

memory = InMemorySaver()

tools = [
    general_question_tool,
    mil_std_rag_tool
]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
    Sen tool kullanabilen bir yapay zeka ajanısın.

    Kullanıcının isteğini değerlendir ve uygun yöntemi seç.

    RKT-MIL-STD-001 teknik dokümanıyla ilgili bir soru sorulursa
    mil_std_rag_tool kullan.

    Genel bilgi veya dokümanla ilgisi olmayan bir soru sorulursa
    general_question_tool kullan.

    Kullanıcının sorusu önceki konuşmada verilen bir bilgi kullanılarak
    cevaplanabiliyorsa konuşma geçmişini kullan.
    """,
    checkpointer=memory
)

config = {
    "configurable": {
        "thread_id": "workshop-user-1"
    }
}

message_count = 0

while True:

    user_input = input("Kullanıcı: ").strip()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config=config
    )

    new_messages = result["messages"][message_count:]

    message_count = len(result["messages"])

    selected_tools = []

    for message in new_messages:

        tool_calls = getattr(
            message,
            "tool_calls",
            None
        )

        if tool_calls:

            for tool_call in tool_calls:
                selected_tools.append(
                    tool_call["name"]
                )

    if selected_tools:
        print(f"Kullanılan tool: {selected_tools}")

    else:
        print("tool kullanılmadı")

    response = result["messages"][-1].content

    print(response)