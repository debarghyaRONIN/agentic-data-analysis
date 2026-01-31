from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import math
import json

from agents.analysis_agent import AnalysisAgent
from agents.fuzzy_agent import FuzzyPredictionAgent
from agents.decision_agent import DecisionAgent
from agents.decision_llm_model import DecisionLLMWrapper

from utils.json_formatter import build_agent_json 


# App setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Utility
def sanitize_dict(d: dict) -> dict:
    cleaned = {}
    for k, v in d.items():
        if isinstance(v, float):
            if math.isnan(v) or math.isinf(v):
                cleaned[k] = 0.0
            else:
                cleaned[k] = round(v, 4)
        else:
            cleaned[k] = v
    return cleaned


# Storage
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"  

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True) 

# Agents (SINGLETONS)
analysis_agent = AnalysisAgent()
fuzzy_agent = FuzzyPredictionAgent()
decision_agent = DecisionAgent(kb_path="rag/knowledge_base.txt")
llm_wrapper = DecisionLLMWrapper(model="mistral")

# Upload dataset
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    analysis_agent.load_data(path)

    return {
        "status": "uploaded",
        "rows": len(analysis_agent.df)
    }

# Raw data preview
@app.get("/data")
def data():
    if analysis_agent.df is None:
        return []

    df = analysis_agent.df.copy()
    df = df.replace([float("inf"), float("-inf")], None)
    df = df.where(df.notna(), None)

    return df.to_dict(orient="records")


# Chat endpoint
@app.post("/chat")
def chat(payload: dict):
    try:
        if analysis_agent.df is None:
            return {"reply": "Please upload a dataset first."}

        user_question = (
            payload.get("message")
            or payload.get("question")
            or payload.get("text")
            or ""
        ).strip()

        if not user_question:
            return {"reply": "Please ask a valid question."}
        
        # Analysis Agent
        summary, charts, df = analysis_agent.analyze()
        summary = sanitize_dict(summary)

        latest = df.iloc[-1]

        volatility_value = (
            charts["volatilityTrend"][-1]
            if charts["volatilityTrend"]
            else 0
        )

        # Fuzzy Logic Agent
        fuzzy = fuzzy_agent.predict(
            rating=float(latest["rating"]),
            volatility=float(volatility_value),
        )

        fuzzy_chart = fuzzy_agent.get_membership_charts()

        # Decision Agent (RAG + LLM)
        rag_context = decision_agent.retrieve_context(
            f"order flow {fuzzy['order_flow_level']} rating {summary['rating_mean']}"
        ) or ["No relevant historical context found."]

        llm_text = llm_wrapper.generate_response(
            user_question=user_question,
            analysis_summary=summary,
            fuzzy_output=fuzzy,
            rag_context=rag_context
        )

        # JSON TEMPLATE (NEW, NON-BREAKING)
        json_template = build_agent_json(
           query=user_question,
           analysis_summary=summary,
           fuzzy_output=fuzzy,
           rag_context=rag_context,
           llm_text=llm_text,
           charts=charts,
           fuzzy_charts=fuzzy_chart
        )

        # save JSON output for Flutter / audit
        with open(
            f"{OUTPUT_DIR}/outputs_{json_template['meta']['request_id']}.json",
            "w"
        ) as f:
            json.dump(json_template, f, indent=2)

        # Response (React + Flutter)
        return {
            "reply": llm_text,            
            "charts": charts,
            "prediction": fuzzy,
            "fuzzy_chart": fuzzy_chart,
            "json_template": json_template,
            "defuzz_value": fuzzy["predicted_order_flow"],  
        }

    except Exception as e:
        print("CHAT ERROR:", e)
        return {"reply": "Something went wrong while analyzing your data."}