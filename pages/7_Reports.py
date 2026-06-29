import streamlit as st

from litelight_core import (
    ensure_state,
    log_to_dataframe,
    make_csv_bytes,
    make_json_bytes,
    make_pdf_bytes,
)

st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")
ensure_state(st)

st.title("Reports")
st.caption("Export lighting logs for procedure review, training, maintenance, and workflow documentation.")

log = st.session_state.lighting_log
df = log_to_dataframe(log)

if df.empty:
    st.info("No lighting log entries yet. Save modes from Procedure Modes, Light Mixer, CureGuard, ShadeLock, or SteriLight.")
else:
    st.subheader("Lighting Log")
    st.dataframe(df, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "Download CSV",
            data=make_csv_bytes(log),
            file_name="litelight_lighting_log.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "Download JSON",
            data=make_json_bytes(log),
            file_name="litelight_lighting_log.json",
            mime="application/json",
            use_container_width=True,
        )

    with col3:
        st.download_button(
            "Download PDF",
            data=make_pdf_bytes(log),
            file_name="litelight_lighting_log.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.divider()

    if st.button("Clear Current Session Log", type="secondary"):
        st.session_state.lighting_log = []
        st.success("Session log cleared.")
        st.rerun()