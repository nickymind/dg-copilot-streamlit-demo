# DG Copilot — Data Governance as Code (AI-Augmented MVP)

Este repositorio implementa un **MVP práctico de Data Governance as Code**, con ejecución real end-to-end.

El objetivo es demostrar cómo el gobierno del dato puede materializarse como un **artefacto de software consumible**, versionado y observable, en lugar de quedar limitado a documentos o marcos teóricos.

No es un framework académico ni un catálogo completo: es un **patrón mínimo, productizable**, pensado para entornos de datos reales y regulados.

---

## Qué problema aborda

En muchos programas de datos existe una brecha persistente entre:

- **Política de Gobierno** (PDFs, comités, lineamientos), y  
- **Implementación Técnica** (pipelines, APIs, plataformas).

Este proyecto explora cómo cerrar esa brecha convirtiendo el output de Data Governance en un **contrato técnico explícito**, entendible por humanos y sistemas.

---

## Qué resuelve

- Genera **metadata de negocio a nivel campo**, incluyendo:
  - definiciones
  - sensibilidad (No-PII / PII / SPII)
  - reglas de calidad
  - notas de linaje y uso
- Identifica **riesgos de privacidad y compliance**.
- Propone **controles mínimos de Data Governance** accionables.
- Usa **BIAN como marco de referencia preferido**, sin forzarlo cuando no aplica.
- Publica el resultado como un **contrato JSON versionado**.
- Permite consumo **ejecutivo y técnico** mediante API + viewer web.

---

## Qué no es

- No es un data catalog enterprise.
- No reemplaza herramientas como Collibra, DataHub u OpenMetadata.
- No define políticas corporativas ni marcos regulatorios formales.

---

## Arquitectura (alto nivel)

```text
Usuario / GPT
   |
   |  (Contrato JSON de Data Governance)
   v
FastAPI — DG Analyzer API
   |
   |  GET /governance/latest
   v
Streamlit — Governance Viewer 
```
	
## Artefacto central: contrato de Data Governance

El núcleo del diseño es un **contrato JSON versionado**, pensado para:

- lectura humana clara,
- validación técnica,
- integración futura con catálogos o pipelines.

### Esquema actual

```json
{
  "analysis_schema_version": "v1",
  "resumen": { ... },
  "campos_metadata": [ ... ],
  "controles": { ... }
}
```

**Por qué así**
- `##` porque es core
- `### Esquema actual` porque es detalle técnico
- El JSON da señal inmediata de ingeniería

---

## 2) **Cómo explorarlo**

También es **sección principal**, pero con sub-opciones claras.

```
## Cómo explorarlo

### Viewer web (recomendado)

Permite revisar el último análisis publicado, con foco ejecutivo y técnico.

👉 https://dg-copilot-app-demo.streamlit.app/

### Ejecución local

```bash
git clone https://github.com/nickymind/dg-copilot-streamlit-demo
cd dg-copilot-streamlit-demo
pip install -r requirements.txt
streamlit run app.py

```
**Por qué así**
- Evita frustración
- Separa público ejecutivo vs técnico
- No obliga a nadie a “correr cosas”

---

## 3) **ADR — Architecture Decision Record**

Esto es **oro senior**, pero tiene que ser sobrio.

```
## ADR — Architecture Decision Record

### ADR-001: Data Governance como contrato JSON versionado

**Estado:** Accepted

**Contexto**  
Las iniciativas de Data Governance suelen fallar cuando el conocimiento queda encapsulado en documentos no integrables con la plataforma de datos.

**Decisión**  
Representar el output de Data Governance como un **contrato JSON explícito, schema-first y versionado**.

**Justificación**
- Permite enforcement técnico.
- Reduce ambigüedad entre negocio y tecnología.
- Es agnóstico a vendors.
- Habilita CI/CD, validaciones y evolución controlada.

**Consecuencias**
- El gobierno del dato se vuelve observable.
- Se facilita la integración progresiva con plataformas reales.
- Se evita lock-in prematuro.

