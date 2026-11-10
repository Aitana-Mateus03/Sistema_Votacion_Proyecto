
import time

from infrastructure.external.circuit_breaker import (
    CircuitBreaker,
    retry_with_backoff
)


def test_circuit_breaker_tres_estados():
    breaker = CircuitBreaker(
        failure_threshold=1,
        recovery_timeout=0.01
    )

    def servicio_fallido():
        raise ValueError("Servicio no disponible")

    try:
        breaker.call(servicio_fallido)
    except ValueError:
        pass

    assert breaker.state == "OPEN"

    time.sleep(0.02)

    resultado = breaker.call(lambda: "Servicio recuperado")

    assert resultado == "Servicio recuperado"
    assert breaker.state == "CLOSED"


def test_reintentos_exponenciales():
    intentos = {"total": 0}

    def servicio_inestable():
        intentos["total"] += 1

        if intentos["total"] < 3:
            raise ValueError("Error temporal")

        return "Correcto"

    resultado = retry_with_backoff(
        servicio_inestable,
        max_attempts=3,
        base_delay=0.01
    )

    assert resultado == "Correcto"
    assert intentos["total"] == 3
