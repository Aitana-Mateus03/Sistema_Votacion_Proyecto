import httpx

from infrastructure.external.circuit_breaker import (
    CircuitBreaker,
    retry_with_backoff
)

class ColombiaApiClient:

    def __init__(self):
        self.http = httpx.Client(timeout=30)

        # Cada API tiene su propio Circuit Breaker
        self.datos_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=10
        )

        self.dane_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=10
        )

    def obtener_datos_abiertos(self):
        def request():
            response = self.http.get(
                "https://www.datos.gov.co/resource/xaxy-8nri.json",
                params={"$limit": 100}
            )
            response.raise_for_status()
            return response.json()

        return self.datos_breaker.call(
            retry_with_backoff,
            request
        )

    def obtener_datos_dane(self):
        def request():
            response = self.http.get(
                "https://geoportal.dane.gov.co/laboratorio/serviciosjson/gdivipola/servicios/total_centros_poblados.php",
                params={"nivel_geografico": "DPTO"}
            )
            response.raise_for_status()
            return response.json()

        return self.dane_breaker.call(
            retry_with_backoff,
            request
        )