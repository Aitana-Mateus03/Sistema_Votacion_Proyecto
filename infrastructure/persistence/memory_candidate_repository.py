from domain.entities.candidate import Candidate
from domain.ports.candidate_repository import CandidateRepository


class MemoryCandidateRepository(CandidateRepository):

    def __init__(self):
        self.candidates = {}

    def save(self, candidate: Candidate) -> Candidate:
        self.candidates[candidate.id] = candidate
        return candidate

    def find_by_id(self, candidate_id: int):
        return self.candidates.get(candidate_id)

    def find_all(self) -> list[Candidate]:
        return list(self.candidates.values())

    def delete(self, candidate_id: int) -> bool:
        if candidate_id in self.candidates:
            del self.candidates[candidate_id]
            return True

        return False