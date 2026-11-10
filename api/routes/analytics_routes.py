
import json

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from infrastructure.external.colombia_api_client import ColombiaApiClient
from infrastructure.external.duckdb_analytics import DuckDBAnalytics

router = APIRouter(tags=["Analitica"])


@router.get("/dashboard/analitica", response_class=HTMLResponse)
def dashboard_analitica(departamento: str = Query(default="Todos")):
    try:
        api = ColombiaApiClient()
        datos = api.obtener_datos_abiertos()

        db = DuckDBAnalytics()
        db.procesar_datos(datos)

        departamentos = db.consulta_por_departamento()

        if departamento == "Todos":
            estadisticas = db.estadisticas()
            tipos = db.consulta_por_tipo()
        else:
            estadisticas = db.estadisticas(departamento)
            tipos = db.consulta_por_tipo(departamento)

        nombres = json.dumps([fila[0] for fila in departamentos])
        cantidades = json.dumps([fila[1] for fila in departamentos])

        nombres_tipos = json.dumps([fila[0] for fila in tipos])
        cantidades_tipos = json.dumps([fila[1] for fila in tipos])

        opciones = "".join(
            f'<option value="{nombre}" {"selected" if nombre == departamento else ""}>{nombre}</option>'
            for nombre, _, _ in departamentos
        )

        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Panel de analítica electoral</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body {{ font-family: Arial; margin: 35px; background: #f3f4f6; }}
                h1 {{ color: #243b53; }}
                .contenedor {{ display: flex; flex-wrap: wrap; gap: 20px; }}
                .tarjeta {{ background: white; padding: 20px; border-radius: 10px;
                            flex: 1; min-width: 250px; }}
                .grafico {{ background: white; padding: 20px; margin-top: 20px;
                            border-radius: 10px; width: 45%; min-width: 300px; }}
                select {{ padding: 10px; margin: 10px 0 20px; min-width: 220px; }}
            </style>
        </head>
        <body>
            <h1>Panel de analítica de centros poblados de Colombia</h1>

            <label for="departamento"><strong>Seleccionar departamento:</strong></label>
            <select id="departamento" onchange="filtrarDepartamento()">
                <option value="Todos" {"selected" if departamento == "Todos" else ""}>
                    Todos los departamentos
                </option>
                {opciones}
            </select>

            <div class="contenedor">
                <div class="tarjeta">
                    <h3>Total de registros</h3>
                    <h2>{estadisticas[0]}</h2>
                </div>
                <div class="tarjeta">
                    <h3>Departamentos</h3>
                    <h2>{estadisticas[1]}</h2>
                </div>
                <div class="tarjeta">
                    <h3>Municipios</h3>
                    <h2>{estadisticas[2]}</h2>
                </div>
            </div>

            <div class="contenedor">
                <div class="grafico">
                    <h3>Centros poblados por departamento</h3>
                    <canvas id="graficoDepartamentos"></canvas>
                </div>
                <div class="grafico">
                    <h3>Distribución por tipo</h3>
                    <canvas id="graficoTipos"></canvas>
                </div>
            </div>

            <script>
                function filtrarDepartamento() {{
                    const departamento =
                        document.getElementById('departamento').value;

                    window.location.href =
                        '/dashboard/analitica?departamento=' +
                        encodeURIComponent(departamento);
                }}

                new Chart(document.getElementById('graficoDepartamentos'), {{
                    type: 'bar',
                    data: {{
                        labels: {nombres},
                        datasets: [{{
                            label: 'Centros poblados',
                            data: {cantidades}
                        }}]
                    }}
                }});

                new Chart(document.getElementById('graficoTipos'), {{
                    type: 'pie',
                    data: {{
                        labels: {nombres_tipos},
                        datasets: [{{
                            data: {cantidades_tipos}
                        }}]
                    }}
                }});
            </script>
        </body>
        </html>
        """

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
