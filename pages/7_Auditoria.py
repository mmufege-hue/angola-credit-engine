"""Página de auditoria e histórico persistido do protótipo."""
from __future__ import annotations

import json
import pandas as pd
import streamlit as st

from database import initialize_database, get_connection, list_analyses
from ui_helpers import apply_global_theme

apply_global_theme()
st.title("7. Auditoria")
st.caption("Registo técnico de pedidos e análises guardados no SQLite local do protótipo.")
initialize_database()

analyses = list_analyses()
if analyses:
    df = pd.DataFrame(analyses)
    if "conditions" in df:
        df["conditions"] = df["conditions"].apply(lambda x: ", ".join(json.loads(x)) if x else "")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Ainda não existem análises guardadas. Execute um pedido na página 1.")

st.subheader("Eventos de auditoria")
conn = get_connection()
try:
    rows = conn.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 100").fetchall()
    events = [dict(r) for r in rows]
finally:
    conn.close()

if events:
    st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)
else:
    st.info("Ainda não existem eventos de auditoria.")

st.warning("Nota: o SQLite local não é armazenamento persistente adequado para produção ou para auditoria regulatória. Em cloud, use uma base de dados gerida.")
