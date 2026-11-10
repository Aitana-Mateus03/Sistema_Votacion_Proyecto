class AcademicService:

    def __init__(self, career_repository, student_repository):
        self.career_repository = career_repository
        self.student_repository = student_repository

    def list_careers(self):
        return self.career_repository.listar_carreras()

    def list_students(self):
        return self.student_repository.listar_estudiantes()