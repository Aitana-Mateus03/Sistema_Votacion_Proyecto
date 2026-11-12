from pydantic import BaseModel, Field


class CandidateCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    propuesta: str = Field(min_length=10, max_length=2000)
    eleccion_id: int = Field(gt=0)


class CandidateResponse(CandidateCreate):
    id: int