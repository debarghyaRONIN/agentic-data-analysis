# Backend - Agentic Data Analysis & Decision System

## Project Overview

This is a **multi-agent AI system** that combines data analysis, fuzzy logic prediction, and LLM-based decision making using Retrieval-Augmented Generation (RAG). The system analyzes business data (specifically sales/order data) to provide intelligent recommendations through a sophisticated pipeline:

**Data Analysis → Fuzzy Logic Prediction → RAG-based Decision Making**

The backend is built with **FastAPI** and exposes REST endpoints that process datasets, analyze trends, predict demand, and generate AI-driven business decisions.

---

## Architecture Overview

The system uses a **three-agent pipeline**:

```
┌─────────────────────┐
│  User Data (CSV)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│  1. ANALYSIS AGENT              │
│  - Load & pre-process data      │
│  - Calculate statistics         │
│  - Extract trends & volatility  │
└──────────┬──────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  2. FUZZY PREDICTION AGENT       │
│  - Fuzzy logic rules (rating,    │
│    time, volatility)            │
│  - Predict order flow levels    │
│  - Generate membership charts   │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  3. DECISION AGENT (RAG + LLM)   │
│  - Retrieve historical knowledge │
│  - Generate contextual response  │
│  - Provide business decisions    │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  JSON Response                   │
│  - Analysis summary              │
│  - Fuzzy predictions             │
│  - RAG context                   │
│  - LLM explanation               │
└──────────────────────────────────┘
```

---

## Project Structure

```
backend/
├── main.py                          # FastAPI application & endpoints
├── app.py                           # Streamlit frontend (alternative UI)
├── requirements.txt                 # Python dependencies
├── data/                            # Sample datasets
│   ├── sales_data.csv
│   ├── sales.csv
│   └── test_*.csv
├── uploads/                         # Directory for user-uploaded CSV files
├── outputs/                         # Directory for generated JSON responses
├── agents/                          # Core AI agents
│   ├── analysis_agent.py           # Data analysis & statistics
│   ├── fuzzy_agent.py              # Fuzzy logic prediction system
│   ├── decision_agent.py           # RAG-based context retrieval
│   └── decision_llm_model.py       # LLM wrapper for decision generation
├── rag/                             # Retrieval-Augmented Generation
│   ├── vector_store.py             # Vector database for semantic search
│   └── knowledge_base.txt          # Business rules & context
└── utils/                           # Utility functions
    └── json_formatter.py            # JSON response builder
```

---

## Agent Descriptions

### 1. **Analysis Agent** (`agents/analysis_agent.py`)

**Purpose**: Loads, pre-processes, and analyzes business data.

**Key Functionality**:
- Loads CSV files and normalizes column names (lowercase, remove spaces)
- Calculates statistical metrics:
  - **Rating Mean**: Average customer rating
  - **Rating Trend**: Increasing/Decreasing trend
  - **Volatility**: Rolling standard deviation (window=3) of ratings
- Generates chart data for visualization

**Key Methods**:
- `load_data(file_path)`: Loads CSV and normalizes columns
- `analyze()`: Returns summary statistics, chart data, and processed DataFrame

**Example Output**:
```json
{
  "rating_mean": 3.85,
  "rating_trend": "increasing",
  "volatility": 0.42,
  "ratingTrend": [3.2, 3.5, 3.8, 4.0, ...],
  "volatilityTrend": [0.3, 0.35, 0.42, ...]
}
```

---

### 2. **Fuzzy Prediction Agent** (`agents/fuzzy_agent.py`)

**Purpose**: Uses fuzzy logic to predict demand/order flow based on real-time inputs.

**Fuzzy Logic System**:

The agent implements a **Fuzzy Control System** with:

#### **Inputs** (Antecedents):
- **Rating** (0-5): Customer satisfaction level
  - Membership sets: `low` (0-3), `medium` (2.5-4.5), `high` (4-5)
  
- **Order Hour** (0-23): Time of day
  - Membership sets: `morning` (0-12), `afternoon` (11-17), `evening` (16-23)
  
- **Volatility** (0-100): Market uncertainty
  - Membership sets: `low` (0-30), `medium` (20-70), `high` (60-100)

#### **Output** (Consequent):
- **Order Flow** (0-300): Expected sales volume
  - Membership sets: `low` (0-120), `medium` (100-200), `high` (180-300)

#### **Fuzzy Rules** (Rule Base):
```
1. IF rating=high AND hour=evening AND volatility=low → order_flow=high
2. IF rating=medium AND hour=afternoon AND volatility=medium → order_flow=medium
3. IF hour=morning → order_flow=low
4. IF volatility=high → order_flow=low
5. IF rating=low → order_flow=low
```

**Defuzzification**: Uses centroid method to convert fuzzy output to crisp values.

**Key Methods**:
- `predict(rating, order_hour, volatility)`: Returns predicted order flow and level
- `get_membership_charts()`: Returns membership function data for visualization

**Example Output**:
```json
{
  "predicted_order_flow": 215.34,
  "order_flow_level": "HIGH"
}
```

---

### 3. **Decision Agent** (`agents/decision_agent.py`)

**Purpose**: Retrieves relevant business context from knowledge base using semantic search (RAG).

**Key Functionality**:
- Uses **VectorStore** for RAG (Retrieval-Augmented Generation)
- Converts text to embeddings using `SentenceTransformer`
- Performs semantic similarity search in FAISS vector index
- Retrieves top-k most relevant business rules or historical insights

**Key Methods**:
- `retrieve_context(query)`: Retrieves k=2 most relevant documents from knowledge base

**Expected RAG Context** (from `knowledge_base.txt`):
- Inventory management rules
- Historical trend insights
- Business decision logic

---

### 4. **Decision LLM Model** (`agents/decision_llm_model.py`)

**Purpose**: Generates intelligent business decisions using an LLM (Mistral) with RAG context.

**Key Functionality**:
- Wraps **Ollama** (local LLM runner) with Mistral model
- Constructs detailed prompts combining:
  - User question
  - Analysis summary (ratings, trends)
  - Fuzzy predictions
  - RAG-retrieved context
- Generates concise, data-driven business recommendations

**System Prompt**:
```
You are a business decision assistant.

RULES:
- Answer ONLY the user's question.
- Use ONLY the provided data.
- DO NOT invent metrics.
- If the data cannot answer the question, say so clearly.
- Be concise and practical.
```

**Key Methods**:
- `generate_response(user_question, analysis_summary, fuzzy_output, rag_context)`: Returns LLM-generated decision text

**Example Output**:
```
"Based on the high rating trend (3.85 avg) and high order flow prediction (215), 
I recommend increasing inventory by 20%. Historical data shows this strategy 
works well in peak demand periods."
```

---

## 🛠️ Vector Store & RAG System

### **Vector Store** (`rag/vector_store.py`)

Implements semantic search using:
- **SentenceTransformer** (`all-MiniLM-L6-v2`): Converts text to 384-dimensional embeddings
- **FAISS** (Facebook AI Similarity Search): Efficient vector indexing & search

**Architecture**:
1. Loads knowledge base text
2. Splits by newlines into individual statements
3. Encodes all texts to embeddings
4. Builds FAISS index for fast similarity search
5. On query: encodes query → searches top-k similar texts → returns matching documents

**Knowledge Base** (`rag/knowledge_base.txt`):
```
If demand is high and ratings are good, increase inventory.
If demand is medium, maintain current inventory.
If demand is low, reduce inventory and focus on marketing.
Historical trend shows inventory increase worked well in high-demand periods.
```

---

## FastAPI Endpoints

### **1. Upload Dataset**
```
POST /upload
Content-Type: multipart/form-data

Request:
- file: CSV file (e.g., sales_data.csv)

Response:
{
  "status": "uploaded",
  "rows": 100
}
```

**Purpose**: Uploads and loads CSV data into the Analysis Agent's DataFrame.

---

### **2. Get Data Preview**
```
GET /data

Response:
[
  {
    "rating": 3.5,
    "order_hour": 14,
    "order_flow": 150,
    ...
  },
  ...
]
```

**Purpose**: Returns raw uploaded data as JSON records.

---

### **3. Chat/Analyze** (Main Endpoint)
```
POST /chat
Content-Type: application/json

Request:
{
  "message": "What should we do with our inventory based on current demand?"
}

Response:
{
  "reply": "Based on the high rating trend (3.85 avg) and high order flow prediction (215), 
            I recommend increasing inventory by 20%...",
  "charts": {
    "ratingTrend": [3.2, 3.5, 3.8, ...],
    "volatilityTrend": [0.3, 0.35, 0.42, ...]
  },
  "prediction": {
    "predicted_order_flow": 215.34,
    "order_flow_level": "HIGH"
  },
  "fuzzy_chart": {
    "rating": {
      "x": [0, 0.1, 0.2, ...],
      "low": [1.0, 0.95, 0.9, ...],
      "medium": [0, 0.05, 0.1, ...],
      "high": [0, 0, 0, ...]
    },
    ...
  },
  "json_template": {
    "meta": {
      "request_id": "uuid",
      "timestamp": "2025-03-17T...",
      "model": "mistral",
      "pipeline": "analysis → fuzzy → decision"
    },
    ...
  },
  "defuzz_value": 215.34
}
```

**Purpose**: Main analysis endpoint that orchestrates all three agents.

**Flow**:
1. Validates dataset is loaded
2. Runs Analysis Agent → gets summary & charts
3. Runs Fuzzy Agent → predicts order flow
4. Runs Decision Agent (RAG) → retrieves context
5. Runs LLM → generates explanation
6. Saves JSON output to `outputs/` directory
7. Returns combined response

---

## Utility Functions

### **JSON Formatter** (`utils/json_formatter.py`)

**Function**: `build_agent_json(query, analysis_summary, fuzzy_output, rag_context, llm_text, charts, fuzzy_charts)`

**Purpose**: Constructs standardized JSON response with:
- **Meta**: Request ID, timestamp, model info, schema version
- **Artifacts**: Declaration of what data is included
- **Input**: Original user query
- **Analysis**: Statistics and trends
- **Prediction**: Fuzzy logic results
- **RAG Context**: Retrieved knowledge
- **Decision**: LLM-generated response
- **Charts**: Data for visualization

**Output Structure**:
```json
{
  "meta": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-03-17T10:30:45.123456",
    "model": "mistral",
    "pipeline": "analysis → fuzzy → decision",
    "schema_version": "1.3"
  },
  "artifacts": {
    "charts": true,
    "fuzzy_membership": true,
    "defuzzification": true,
    "chat_response": true
  },
  "input": {
    "query": "What should we do with inventory?",
    "context_used": true
  },
  "analysis": { ... },
  "prediction": { ... },
  "rag": { ... },
  "decision": { ... }
}
```

---

## Data Flow Example

**Input CSV** (`sales_data.csv`):
```
rating,order_hour,order_flow
3.2,8,120
3.5,12,140
3.8,14,150
4.0,18,200
```

**Step 1: Analysis Agent**
- Loads data
- Calculates: rating_mean=3.625, volatility=0.32, trend=increasing

**Step 2: Fuzzy Agent**
- Input: rating=4.0, order_hour=18, volatility=0.32
- Applies fuzzy rules
- Output: predicted_order_flow=220, level=HIGH

**Step 3: Decision Agent (RAG)**
- Query: "order flow HIGH rating 3.625"
- Retrieves: "If demand is high and ratings are good, increase inventory."

**Step 4: LLM Decision**
- Generates: "Based on high ratings and demand, increase inventory by 20%."

**Output**: JSON with all analysis, prediction, context, and decision data.

---

## How to Run

### **Prerequisites**
- Python 3.8+
- pip

### **Installation**
```bash
cd backend
pip install -r requirements.txt
```

### **Run FastAPI Server**
```bash
python main.py
```

Server starts at `http://localhost:8000`

API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### **Run Streamlit Frontend** (Alternative)
```bash
streamlit run app.py
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| **fastapi** | REST API framework |
| **uvicorn** | ASGI server for FastAPI |
| **pandas** | Data manipulation & analysis |
| **numpy** | Numerical computing |
| **scikit-fuzzy** | Fuzzy logic system |
| **scikit-learn** | ML utilities |
| **sentence-transformers** | Text embeddings for RAG |
| **faiss-cpu** | Vector search index |
| **ollama** | Local LLM runner (Mistral) |
| **streamlit** | Alternative interactive UI |
| **plotly** | Interactive visualizations |

See `requirements.txt` for full list.

---

## Key Features

- **Multi-Agent Pipeline**: Seamlessly combines analysis, fuzzy logic, and LLM reasoning

- **Fuzzy Logic**: Rule-based predictions with uncertainty handling

- **RAG (Retrieval-Augmented Generation)**: Uses semantic search to ground LLM responses in business knowledge

- **REST API**: Easy integration with frontend applications

- **JSON Artifacts**: Structured output for Flutter, React, or other clients

- **CORS Support**: Configured for frontend at `http://localhost:3000`

- **Data Persistence**: Saves all analysis outputs to `outputs/` directory with unique request IDs

---

## Example Use Cases

1. **Inventory Management**: "Should we increase inventory based on current trends?"
2. **Demand Forecasting**: "What's the expected order flow for tomorrow evening?"
3. **Quality Analysis**: "How stable are our customer ratings?"
4. **Sales Strategy**: "What actions do you recommend given current market conditions?"

---

## Future Enhancements

- Real-time streaming data support
- Additional fuzzy rule customization UI
- Multi-model LLM support (GPT-4, Claude, etc.)
- Advanced time-series analysis
- Batch processing for large datasets
- Model training pipeline for custom fuzzy rules

---

## Notes

- **Knowledge Base**: Customize `rag/knowledge_base.txt` with your business rules
- **LLM Model**: Requires Ollama with Mistral model installed (`ollama pull mistral`)
- **CORS**: Update `allow_origins` in `main.py` if frontend runs on different origin
- **Embeddings**: Uses pre-trained `all-MiniLM-L6-v2` (384 dimensions)

---

**Built with**: FastAPI + Fuzzy Logic + RAG + LLM Reasoning
