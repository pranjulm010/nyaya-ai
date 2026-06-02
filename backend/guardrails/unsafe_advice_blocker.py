from core.llm_router import run_llm


SAFETY_PROMPT = """
You are a legal safety classifier.

Determine if the user query seeks:

UNSAFE:
- illegal help
- evading law
- destroying evidence
- hiding crime
- witness tampering
- fraud
- fake legal documents
- misleading court
- criminal assistance

SAFE:
- legal rights
- legal defence
- criminal law explanation
- legal procedure
- lawful guidance

Return only:

SAFE
or
UNSAFE

Query:
{query}
"""


def is_unsafe_query(query: str) -> bool:
    if not query or not query.strip():
        return False

    try:
        result = run_llm(
            prompt=SAFETY_PROMPT.format(query=query),
            intent="simple_legal",
            temperature=0
        )

        return result.strip().upper() == "UNSAFE"

    except Exception:
        return False