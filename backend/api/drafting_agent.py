from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def drafting_agent(prompt):

    strict_prompt = f"""
    You are Nyaya AI.

    IMPORTANT RULES:

    - Answer ONLY from the provided context
    - Do NOT use your own knowledge
    - Do NOT hallucinate
    - Do NOT assume facts
    - If answer is not present in context,
      say:
      "I could not find this information in the provided sources."

    PROVIDED CONTEXT:
    {prompt}

    FINAL ANSWER:
    """

    response = llm.invoke(
        strict_prompt
    )

    return response.content