from typing import Dict, Any

OUT_OF_DOMAIN_MESSAGE = (
    "This question is out of my legal domain. "
    "Please ask a law or legal-related question."
)


LEGAL_CLASSIFIER_PROMPT = """
You are a strict domain classifier for an Indian Legal AI.

Task:
Classify the user query as LEGAL or NON_LEGAL.

LEGAL means:
- law
- court
- constitution
- IPC/BNS/BNSS/BSA
- police/legal rights
- contracts
- property disputes
- divorce/family law
- criminal/civil cases
- legal drafting
- legal procedure
- legal research

NON_LEGAL means:
- programming
- Python/code/debugging
- cooking
- sports
- weather
- medical
- general knowledge
- finance
- education
- anything not related to law

Important:
The query may be in any language.
Understand the meaning, not just keywords.

Return only one word:
LEGAL
or
NON_LEGAL

Query:
{query}
"""


def classify_legal_domain(query: str, llm) -> str:
    if not query or not query.strip():
        return "NON_LEGAL"

    prompt = LEGAL_CLASSIFIER_PROMPT.format(query=query)

    try:
        result = llm.invoke(prompt)

        if hasattr(result, "content"):
            label = result.content.strip().upper()
        else:
            label = str(result).strip().upper()

        if "LEGAL" == label:
            return "LEGAL"

        return "NON_LEGAL"

    except Exception:
        # Fail closed: do not answer if classifier fails
        return "NON_LEGAL"


def out_of_domain_response(query: str) -> Dict[str, Any]:
    return {
        "blocked": True,
        "safe_query": query,
        "safe_sources": [],
        "confidence": "High",
        "disclaimer": "",
        "reason": "out_of_legal_domain",
        "message": OUT_OF_DOMAIN_MESSAGE
    }