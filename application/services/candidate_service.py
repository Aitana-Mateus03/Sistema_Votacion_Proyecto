from domain.entities.candidate import Candidate
from domain.ports.candidate_repository import CandidateRepository


class CandidateService:

    def __init__(self, repository: CandidateRepository):
        self.repository = repository

    def create_candidate(
        self,
        candidate_id: int,
        nombre: str,
        propuesta: str,
        eleccion_id: int
    ) -> Candidate:

        candidate = Candidate(
            id=candidate_id,
            nombre=nombre,
            propuesta=propuesta,
            eleccion_id=eleccion_id
        )

        return self.repository.save(candidate)

    def get_candidate(self, candidate_id: int):
        return self.repository.find_by_id(candidate_id)

    def get_all_candidates(self):
        return self.repository.find_all()

    def delete_candidate(self, candidate_id: int):
        return self.repository.delete(candidate_id)