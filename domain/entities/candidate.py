from dataclasses import dataclass


@dataclass
class Candidate:
    id: int
    nombre: str
    propuesta: str
    eleccion_id: int