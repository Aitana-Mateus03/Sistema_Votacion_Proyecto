from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.candidate import Candidate


class CandidateRepository(ABC):

    @abstractmethod
    def save(self, candidate: Candidate) -> Candidate:
        pass

    @abstractmethod
    def find_by_id(self, candidate_id: int) -> Optional[Candidate]:
        pass

    @abstractmethod
    def find_all(self) -> list[Candidate]:
        pass

    @abstractmethod
    def delete(self, candidate_id: int) -> bool:
        pass