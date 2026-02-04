# DG Copilot – Data Governance Practical Viewer

Este repositorio implementa un **copiloto práctico de Data Governance** que genera, publica y visualiza metadata de negocio y controles mínimos de gobierno del dato a partir de datasets reales o de ejemplo.

El objetivo es **didáctico y aplicado**: mostrar cómo pasar de datos crudos a un artefacto accionable de Data Governance, alineado a buenas prácticas de la industria.

---

## Qué resuelve

- Genera **metadata de negocio por campo** (definiciones, sensibilidad, calidad, linaje).
- Identifica **riesgos de privacidad y compliance** (PII / SPII).
- Propone **controles mínimos de Data Governance** accionables.
- Usa **BIAN como marco de referencia preferido**, sin forzarlo cuando no aplica.
- Publica y visualiza el resultado en un **viewer web**.

---

## Arquitectura (alto nivel)

Usuario / GPT
|
| (JSON de Data Governance)
v
FastAPI (DG Analyzer API)
|
| /governance/latest
v
Streamlit Viewer


- **GPT / Copilot**: genera el análisis de Data Governance.
- **API (FastAPI)**: recibe y persiste el análisis como contrato JSON.
- **Viewer (Streamlit)**: muestra Resumen, Metadata por campo, Controles y JSON completo.

---

## Contrato de datos (analysis)

El viewer consume un objeto `analysis` con el siguiente esquema estable (`v1`):

- `analysis_schema_version` (string, `"v1"`)
- `resumen` (object)
- `campos_metadata` (array de objects)
- `controles` (object)

Este contrato es explícito y versionado para evitar roturas futuras.

---

## Uso típico

1. Generar un análisis de Data Governance (manual o vía GPT).
2. Publicarlo en la API (`/governance/analyze`).
3. Visualizar el último análisis en el Streamlit Viewer.

---

## Contexto de uso

- Curso de **Data Governance / Data Management**.
- Ejercicio práctico de catalogación de datos.
- Demo conceptual de “Data Governance as a Product”.
- Portfolio técnico-profesional.

---

## Nota

Este proyecto **no reemplaza asesoramiento legal o regulatorio**.
Los controles propuestos son mínimos y orientativos, pensados para enseñanza y discusión técnica.
