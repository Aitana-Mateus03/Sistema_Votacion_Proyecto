
import os

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv

from api.routes.candidate_routes import router as candidate_router
from api.routes.analytics_routes import router as analytics_router
from api.auth.routes import router as auth_router

load_dotenv()

app = FastAPI(
    title="Voting System REST API",
    description="API REST for Student Voting System project at UMB",
    version="1.0.0"
)

app.include_router(candidate_router)
app.include_router(analytics_router)
app.include_router(auth_router)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class ProposalAnalysisRequest(BaseModel):
    propuesta: str = Field(min_length=10, max_length=2000)

@app.post("/api/v1/ai/analizar-propuesta")
def analizar_propuesta_ai(payload: ProposalAnalysisRequest):
    try:
        prompt = (
            "Eres un comité de evaluación electoral estudiantil de la UMB. "
            "Analiza objetivamente la siguiente propuesta de candidato y "
            "entrégame un resumen en máximo dos frases cortas indicando "
            "su viabilidad:\n\n"
            f"Propuesta: {payload.propuesta}"
        )

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )

        return {
            "status": "success",
            "propuesta_original": payload.propuesta,
            "analisis_ia": response.text.strip()
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No fue posible analizar la propuesta en este momento."
        )