import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
from google import genai
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env local
load_dotenv()

app = FastAPI(
    title="Voting System REST API",
    description="API REST for Student Voting System project at UMB",
    version="1.0.0"
)

# Configuración oficial de Google GenAI leyendo de la variable de entorno segura
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Modelo de datos para el Candidato
class CandidateCreate(BaseModel):
    nombre: str
    propuesta: str
    eleccion_id: int

class CandidateResponse(CandidateCreate):
    id: int

# Modelo de datos para la solicitud de IA
class ProposalAnalysisRequest(BaseModel):
    propuesta: str

# Base de datos simulada en memoria
db_candidatos = [
    {"id": 1, "nombre": "Rayo McQueen", "propuesta": "Mejorar laboratorios de sistemas", "eleccion_id": 101}
]

# 1. CREATE: Registrar candidato (HTTP 201)
@app.post("/api/v1/candidatos", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
def crear_candidato(candidato: CandidateCreate):
    nuevo_id = len(db_candidatos) + 1
    nuevo_candidato = {**candidato.model_dump(), "id": nuevo_id}
    db_candidatos.append(nuevo_candidato)
    return nuevo_candidato

# 2. READ ALL: Listar candidatos (HTTP 200)
@app.get("/api/v1/candidatos", response_model=List[CandidateResponse])
def listar_candidatos():
    return db_candidatos

# 3. READ BY ID: Obtener detalle (HTTP 200 / 404)
@app.get("/api/v1/candidatos/{candidato_id}", response_model=CandidateResponse)
def obtener_candidato(candidato_id: int):
    for c in db_candidatos:
        if c["id"] == candidato_id:
            return c
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidato no encontrado")

# 4. UPDATE: Actualizar candidato (HTTP 200 / 404)
@app.put("/api/v1/candidatos/{candidato_id}", response_model=CandidateResponse)
def actualizar_candidato(candidato_id: int, datos: CandidateCreate):
    for idx, c in enumerate(db_candidatos):
        if c["id"] == candidato_id:
            actualizado = {**datos.model_dump(), "id": candidato_id}
            db_candidatos[idx] = actualizado
            return actualizado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidato no encontrado")

# 5. DELETE: Eliminar candidato (HTTP 204)
@app.delete("/api/v1/candidatos/{candidato_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_candidato(candidato_id: int):
    for idx, c in enumerate(db_candidatos):
        if c["id"] == candidato_id:
            db_candidatos.pop(idx)
            return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidato no encontrado")

# 6. AI INTEGRATION: Analizar propuesta con Google Gemini oficial (HTTP 200 / 503)
@app.post("/api/v1/ai/analizar-propuesta")
def analizar_propuesta_ai(payload: ProposalAnalysisRequest):
    try:
        prompt = (
            "Eres un comité de evaluación electoral estudiantil de la UMB. "
            "Analiza objetivamente la siguiente propuesta de candidato y entrégame un resumen "
            "en máximo dos frases cortas indicando su viabilidad:\n\n"
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error al conectar con el servicio de IA: {str(e)}"
        )