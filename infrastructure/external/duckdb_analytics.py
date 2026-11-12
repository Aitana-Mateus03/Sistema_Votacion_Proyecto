import duckdb

class DuckDBAnalytics:

    def __init__(self):
        self.connection = duckdb.connect(":memory:")

    def procesar_datos(self, datos):

        self.connection.execute("""
            CREATE OR REPLACE TABLE centros_poblados (
                codigo_departamento VARCHAR,
                nombre_departamento VARCHAR,
                codigo_municipio VARCHAR,
                nombre_municipio VARCHAR,
                codigo_centro_poblado VARCHAR,
                nombre_centro_poblado VARCHAR,
                tipo_centro_poblado VARCHAR,
                longitud VARCHAR,
                latitud VARCHAR
            )
        """)

        columnas = [
            "codigo_departamento",
            "nombre_departamento",
            "codigo_municipio",
            "nombre_municipio",
            "codigo_centro_poblado",
            "nombre_centro_poblado",
            "tipo_centro_poblado",
            "longitud",
            "latitud"
        ]

        valores = [
            tuple(str(registro.get(columna, "")) for columna in columnas)
            for registro in datos
        ]

        if valores:
            self.connection.executemany("""
                INSERT INTO centros_poblados VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, valores)

        return len(valores)

    def consulta_por_departamento(self):
        return self.connection.execute("""
            SELECT
                nombre_departamento,
                COUNT(*) AS total_centros,
                COUNT(DISTINCT codigo_municipio) AS total_municipios
            FROM centros_poblados
            GROUP BY nombre_departamento
            ORDER BY total_centros DESC
        """).fetchall()

    def consulta_por_tipo(self, departamento=None):
        return self.connection.execute("""
            SELECT
                tipo_centro_poblado,
                COUNT(*) AS total
            FROM centros_poblados
            WHERE (? IS NULL OR nombre_departamento = ?)
            GROUP BY tipo_centro_poblado
            ORDER BY total DESC
        """, [departamento, departamento]).fetchall()

    def estadisticas(self, departamento=None):
        return self.connection.execute("""
            SELECT
                COUNT(*) AS total_registros,
                COUNT(DISTINCT codigo_departamento) AS departamentos,
                COUNT(DISTINCT codigo_municipio) AS municipios
            FROM centros_poblados
            WHERE (? IS NULL OR nombre_departamento = ?)
        """, [departamento, departamento]).fetchone()
    