
from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.candidate_schemas import (
    CandidateCreate,
    CandidateResponse
)

from application.services.candidate_service import CandidateService

from infrastructure.persistence.memory_candidate_repository import (
    MemoryCandidateRepository
)

from api.auth.dependencies import require_role


router = APIRouter(
    prefix="/api/v1/candidatos",
    tags=["Candidatos"]
)

repository = MemoryCandidateRepository()


def get_candidate_service():
    return CandidateService(repository)


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_candidato(
    candidato: CandidateCreate,
    current_user: dict = Depends(require_role("ADMIN")),
    service: CandidateService = Depends(get_candidate_service)
):
    return service.create_candidate(
        candidate_id=len(service.get_all_candidates()) + 1,
        nombre=candidato.nombre,
        propuesta=candidato.propuesta,
        eleccion_id=candidato.eleccion_id
    )


@router.get("", response_model=list[CandidateResponse])
def listar_candidatos(
    service: CandidateService = Depends(get_candidate_service)
):
    return service.get_all_candidates()


@router.get("/{candidato_id}", response_model=CandidateResponse)
def obtener_candidato(
    candidato_id: int,
    service: CandidateService = Depends(get_candidate_service)
):
    candidate = service.get_candidate(candidato_id)

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidato no encontrado"
        )

    return candidate


@router.delete(
    "/{candidato_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_candidato(
    candidato_id: int,
    current_user: dict = Depends(require_role("ADMIN")),
    service: CandidateService = Depends(get_candidate_service)
):
    if not service.delete_candidate(candidato_id):
        raise HTTPException(
            status_code=404,
            detail="Candidato no encontrado"
        )

    return None
