# api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.review_graph import run_review

app = FastAPI(title="AI Code Review API", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

class ReviewRequest(BaseModel):
    pr_url: str

@app.get("/")
def root():
    return {"status": "Code Review API running", "endpoint": "POST /review"}

@app.post("/review")
def review(request: ReviewRequest):
    try:
        report = run_review(request.pr_url)
        return {"report": report, "status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
