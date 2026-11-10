from pydantic import BaseModel


class CandidateCreate(BaseModel):
    nombre: str
    propuesta: str
    eleccion_id: int


class CandidateResponse(CandidateCreate):
    id: int