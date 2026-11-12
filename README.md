![CI/CD Pipeline](https://github.com/Aitana-Mateus03/Sistema_Votacion_Proyecto/actions/workflows/ci.yml/badge.svg)

# Sistema de Votación Electrónica — Guía 7 (UMB)

Proyecto de ingeniería de software desarrollado bajo los principios de **Clean Architecture** y buenas prácticas de seguridad y pruebas automatizadas en **FastAPI**.

---

##  Características Principales
- **Arquitectura Limpia:** Separación por capas (Dominio, Aplicación, Infraestructura y API).
- **Seguridad y Autenticación:** 
  - Autenticación robusta basada en **JWT (JSON Web Tokens)**.
  - Control de Acceso Basado en Roles (**RBAC**) con perfiles `ADMIN` y `USER`.
  - Encriptación segura de credenciales mediante `bcrypt`.
- **Pruebas y Calidad de Código:**
  - Suite completa de pruebas unitarias y de integración implementada con `pytest`.
  - Cobertura de código superior al **95%**, superando el umbral mínimo exigido.
  - Validación de mutaciones y robustez de código.
- **CI/CD Automatizado:**
  - Pipeline de integración continua configurado en **GitHub Actions** (`ci.yml`).
  - Control de calidad automatizado con validación estricta de cobertura (`--fail-under=60`).

---

## Tecnologías Utilizadas
* **Python / FastAPI** (Framework backend)
* **Pytest & Coverage** (Pruebas unitarias y reporte de cobertura)
* **GitHub Actions** (CI/CD Pipeline)
* **JWT & Passlib** (Seguridad y autenticación)
* **SQLAlchemy** (ORM de base de datos)