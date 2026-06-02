def no_source_response(query: str = "") -> dict[str, any]:
    """
    LLM-based safe fallback when no verified sources are found.

    Used for practical legal emergency/help queries where
    general lawful guidance can be given without citations.
    """

    try:
        prompt = f"""
You are Nyaya AI, an Indian Legal Safety Assistant.

The system could not find verified API/web/document sources.

User query:
{query}

Task:
Decide if this is a safe general legal-help question.

Examples of safe questions:
- theft happened
- phone snatched
- domestic violence
- police complaint
- FIR process
- cyber fraud
- lost documents
- accident
- harassment

Unsafe questions:
- how to hide crime
- how to destroy evidence
- how to escape police
- how to forge documents
- how to threaten witness

If SAFE, give a short practical answer in the user's language.
If UNSAFE, refuse safely.

Rules:
1. Do not cite fake sources.
2. Do not invent sections/cases.
3. Do not give illegal advice.
4. Give immediate lawful steps.
5. Mention police emergency number 112 where relevant.
6. Mention that user should contact nearest police station/lawyer when needed.
7. Keep answer practical.
8. Return only the final answer.
"""

        fallback_answer = run_llm(
            prompt=prompt,
            intent="simple_legal",
            temperature=0
        )

        return {
            "summary": fallback_answer[:300],
            "answer": fallback_answer,
            "sources_used": [],
            "confidence": "Low",
            "disclaimer": legal_disclaimer(),
            "raw_answer": fallback_answer
        }

    except Exception:
        return {
            "summary": "I could not verify this from the available sources.",
            "answer": (
                "I could not find reliable document, API, or web source context "
                "to answer this question safely."
            ),
            "sources_used": [],
            "confidence": "Low",
            "disclaimer": legal_disclaimer(),
            "raw_answer": (
                "I could not verify this from the available sources."
            )
        }