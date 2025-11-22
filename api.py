from fastapi import FastAPI
from pydantic import BaseModel
from shl_recommender import recommend_assessments

app = FastAPI(title="SHL Assessment Recommendation API")

class QueryRequest(BaseModel):
    job_title: str
    seniority: str
    use_case: str

@app.post("/recommend")
def get_recommendations(req: QueryRequest):
    results = recommend_assessments(req.job_title, req.seniority, req.use_case)
    output = []

    for score, a in results:
        output.append({
            "name": a['name'],
            "score": score,
            "category": a['category'],
            "best_for": a['best_for_roles'],
            "levels": a['level'],
            "use_cases": a['use_cases'],
            "duration": a['duration_min'],
            "description": a["description"]
        })

    return {"recommendations": output}