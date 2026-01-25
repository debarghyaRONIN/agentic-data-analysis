import ollama
from typing import Dict, List


class DecisionLLMWrapper:
    """
    Uses a LOCAL LLM (Ollama) to generate a response
    grounded strictly in agent outputs.
    """

    def __init__(self, model: str = "mistral"):
        self.model = model

        self.system_prompt = """
You are a business decision assistant.

RULES:
- Answer ONLY the user's question.
- Use ONLY the provided data.
- DO NOT invent metrics.
- If the data cannot answer the question, say so clearly.
- Be concise and practical.
"""

    def generate_response(
        self,
        user_question: str,
        analysis_summary: Dict,
        fuzzy_output: Dict,
        rag_context: List[str],
    ) -> str:

        prompt = f"""
USER QUESTION
-------------
{user_question}

BUSINESS DATA
-------------
Customer rating trend: {analysis_summary['rating_trend']}
Average customer rating: {analysis_summary['rating_mean']}
Rating volatility: {analysis_summary['volatility']}

Predicted order flow: {fuzzy_output['predicted_order_flow']}
Predicted order flow level: {fuzzy_output['order_flow_level']}

RETRIEVED CONTEXT
-----------------
{chr(10).join(rag_context)}

TASK
----
Answer the USER QUESTION using ONLY the information above.
If the question cannot be answered from the data, say that clearly.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0.2},
        )

        return response["message"]["content"].strip()