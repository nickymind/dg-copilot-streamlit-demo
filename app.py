import json
import os
import time
import requests
import streamlit as st
from datetime import datetime

# ======================
# Config
# ======================
API_BASE = os.getenv("API_BASE", "https://dg-analyzer-api.onrender.com")
LATEST_URL = f"{API_BASE}/governance/latest"
HEALTH_URL = f"{API_BASE}/health"

st.set_page_config(page_title="DG Viewer", layout="wide")
st.title("DG Viewer")
st.caption(f"Source: {LATEST_URL}")

# ======================
# Helpers
# ======================
@st.cache_data(ttl=10)
def fetch_latest():
    """
    Robust fetch with warmup + retries to handle Render cold starts.
    """
    last_err = None
    for attempt, timeout_s in enumerate([10, 20, 40], start=1):
        try:
            # Warm up API (Render cold start)
            requests.get(HEALTH_URL, timeout=10)

            r = requests.get(LATEST_URL, timeout=timeout_s)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            time.sleep(1.5 * attempt)
    raise last_err


def safe_json_loads(maybe_json):
    if isinstance(maybe_json, str):
        try:
            return json.loads(maybe_json)
        except Exception:
            return {"_raw": maybe_json}
    return maybe_json


# ======================
# UI controls
# ======================
if st.button("Refresh now"):
    st.cache_data.clear()

# ======================
# Load data
# ======================
try:
    payload = fetch_latest()
except Exception as e:
    st.error(f"No se pudo leer /governance/latest. Error: {e}")
    st.stop()

if payload.get("status") == "empty":
    st.warning("Todavía no hay análisis publicado desde el GPT.")
    st.json(payload)
    st.stop()

dataset = payload.get("dataset", "unknown")
timestamp = payload.get("timestamp", "")
analysis = safe_json_loads(payload.get("analysis", {}))

# ======================
# Header metrics
# ======================
col1, col2, col3 = st.columns(3)
col1.metric("Dataset", dataset)
col2.metric("Timestamp (UTC)", timestamp or "n/a")
col3.metric("API", API_BASE)

st.divider()

# ======================
# Tabs
# ======================
tabs = st.tabs(
    ["Resumen", "Campos (metadata)", "Controles", "JSON completo"]
)

with tabs[0]:
    st.subheader("Resumen ejecutivo")
    resumen = analysis.get("resumen_ejecutivo", {})
    if resumen:
        st.json(resumen)
    else:
        st.info("No se encontró `resumen_ejecutivo`.")

with tabs[1]:
    st.subheader("Metadata a nivel campo")
    fields = analysis.get("metadata_campos", [])
    if isinstance(fields, list) and fields:
        st.dataframe(fields, use_container_width=True)
    else:
        st.info("No se encontró `metadata_campos` como lista.")

with tabs[2]:
    st.subheader("Controles mínimos de Data Governance")
    controles = analysis.get("controles_gobierno_minimo", {})
    if controles:
        st.json(controles)
    else:
        st.info("No se encontró `controles_gobierno_minimo`.")

with tabs[3]:
    st.subheader("JSON completo")
    st.json(analysis)

    json_bytes = json.dumps(
        analysis, ensure_ascii=False, indent=2
    ).encode("utf-8")

    st.download_button(
        label="Descargar JSON",
        data=json_bytes,
        file_name=f"dg_analysis_{dataset}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
    )

