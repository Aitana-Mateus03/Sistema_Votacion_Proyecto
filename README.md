# Student Voting System — Academic Project (UMB)

[![CI/CD Pipeline](https://github.com/Aitana-Mateus03/Sistema_Votacion_Proyecto/actions/workflows/ci.yml/badge.svg)](https://github.com/Aitana-Mateus03/Sistema_Votacion_Proyecto/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

##  Overview
The **Student Voting System** is a robust, secure, and highly scalable backend REST API developed for student elections at Universidad Manuela Beltrán. The project follows Clean Architecture principles, ensuring a strict separation of concerns across domains, application layers, infrastructure, and API interfaces. It integrates comprehensive automated testing, robust security measures, and AI capabilities.

##  Live Demo & Production
- **Production API URL:** [https://sistema-votacion-proyecto.onrender.com](https://sistema-votacion-proyecto.onrender.com)
- **Interactive Swagger Documentation:** [https://sistema-votacion-proyecto.onrender.com/docs](https://sistema-votacion-proyecto.onrender.com/docs)

##  Architecture & Tech Stack
- **Backend Framework:** Python with **FastAPI** for high-performance asynchronous routing.
- **Database & ORM:** MySQL managed through **SQLAlchemy 2.0**.
- **Security & Authentication:** 
  - Robust **JWT (JSON Web Tokens)** session management.
  - Role-Based Access Control (**RBAC**) supporting `ADMIN` and `USER` profiles.
  - Secure credential hashing using `bcrypt`.
- **Testing & Quality Assurance:** 
  - Unit and integration testing suite powered by `pytest`.
  - Code coverage thresholds exceeding 95% enforcement.
- **CI/CD Automation:** 
  - Fully automated 4-stage pipeline configured with **GitHub Actions**.
- **Cloud Infrastructure & Containerization:** 
  - Containerized with **Docker** and published to **Docker Hub** (`aitana03/sistema-votacion`).
  - Deployed in production via **Render** PaaS platform.

##  CI/CD Pipeline Workflow
The automated integration and deployment workflow (`ci.yml`) is divided into four critical stages:
1. **Test & Coverage (`test`):** Initializes the testing environment, injects secure environment variables, runs unit tests via `pytest`, and computes code coverage metrics.
2. **Build Image (`build`):** Compiles and packages the application container using optimized Docker multi-stage builds.
3. **Push to Docker Hub (`push`):** Authenticates using secure encrypted repository secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) to publish the latest image tag automatically.
4. **Deploy to PaaS (`deploy`):** Triggers a seamless update in the production cloud environment hosted on Render.

##  Key Features & Endpoints
- **Candidates Management:** Complete CRUD operations for electoral candidates.
- **Analytics Dashboard:** Real-time data processing and vote tracking.
- **Gemini AI Integration:** Advanced analytical features powered by Google AI Studio.
- **Authentication Module:** Secure login, token generation, and role verification.

## Local Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Aitana-Mateus03/Sistema_Votacion_Proyecto.git](https://github.com/Aitana-Mateus03/Sistema_Votacion_Proyecto.git)
   cd Sistema_Votacion_Proyecto