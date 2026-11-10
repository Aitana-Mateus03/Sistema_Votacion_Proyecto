from unittest.mock import MagicMock

from domain.entities.candidate import Candidate
from application.services.candidate_service import CandidateService
from application.services.academic_service import AcademicService


def test_create_candidate_with_mock():
    repository = MagicMock()
    repository.save.side_effect = lambda candidate: candidate

    service = CandidateService(repository)

    candidate = service.create_candidate(
        1,
        "Camila",
        "Mejorar los laboratorios",
        101
    )

    repository.save.assert_called_once()
    assert candidate.nombre == "Camila"
    assert candidate.id == 1


def test_get_candidate_with_mock():
    repository = MagicMock()
    expected = Candidate(
        1, "Carlos", "Mejorar la biblioteca", 101
    )
    repository.find_by_id.return_value = expected

    service = CandidateService(repository)
    result = service.get_candidate(1)

    assert result == expected
    repository.find_by_id.assert_called_once_with(1)


def test_academic_service_with_mocks():
    career_repository = MagicMock()
    student_repository = MagicMock()

    career_repository.listar_carreras.return_value = ["Ingeniería"]
    student_repository.listar_estudiantes.return_value = ["Carlos"]

    service = AcademicService(
        career_repository,
        student_repository
    )

    assert service.list_careers() == ["Ingeniería"]
    assert service.list_students() == ["Carlos"]