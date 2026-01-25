import uuid
from datetime import datetime

def build_agent_json(
    query,
    analysis_summary,
    fuzzy_output,
    rag_context,
    llm_text
):
    return {
        "meta": {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "model": "mistral",
            "pipeline": "analysis → fuzzy → decision"
        },
        "input": {
            "query": query,
            "context_used": bool(rag_context)
        },
        "analysis_agent": {
            "summary": analysis_summary,
            "confidence": analysis_summary.get("confidence", 0.0)
        },
        "fuzzy_prediction_agent": {
            "inputs": {
                "rating": analysis_summary.get("rating_mean"),
                "volatility": fuzzy_output.get("volatility", 0.0)
            },
            "fuzzy_state": fuzzy_output.get("order_flow_level"),
            "predicted_score": fuzzy_output.get("score", 0.0)
        },
        "decision_agent": {
            "decision": fuzzy_output.get("decision", "REVIEW"),
            "reasoning": llm_text,
            "supporting_docs": rag_context
        },
        "final_output": {
            "text": llm_text,
            "actionable_steps": []
        }
    }