import streamlit as st

from litelight_core import (
    AUTHOR,
    PRODUCT_NAME,
    PURPOSE,
    add_log,
    assess_light_risk,
    build_device_payload,
    ensure_state,
    get_presets,
    set_mode,
    settings_to_dataframe,
)

st.set_page_config(
    page_title="Litelight Specialty Lighting",
    page_icon="💡",
    layout="wide",
)

ensure_state(st)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #5f6368;
        margin-bottom: 1rem;
    }
    .litelight-card {
        padding: 1rem;
        border: 1px solid #e6e8eb;
        border-radius: 16px;
        background: #fbfcff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"<div class='main-title'>{PRODUCT_NAME}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>Purpose: {PURPOSE} · Author: {AUTHOR}</div>", unsafe_allow_html=True)

presets = get_presets()

with st.sidebar:
    st.header("Clinic Setup")
    st.session_state.active_operatory = st.text_input("Operatory", st.session_state.active_operatory)
    st.session_state.dentist_name = st.text_input("Dentist", st.session_state.dentist_name)
    st.session_state.assistant_name = st.text_input("Assistant", st.session_state.assistant_name)

    st.divider()
    st.session_state.device_online = st.toggle("Device bridge online", st.session_state.device_online)

st.info(
    "Litelight treats lighting as an active dental workflow layer: procedure modes, presets, "
    "safety prompts, shade support, cleaning support, and documentation logs."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Procedure Modes", len(presets))
col2.metric("Current Mode", st.session_state.current_mode)
col3.metric("Lighting Logs", len(st.session_state.lighting_log))
col4.metric("Device Bridge", "Online" if st.session_state.device_online else "Simulated")

st.subheader("Quick Procedure Mode Loader")

selected_mode = st.selectbox(
    "Select procedure mode",
    list(presets.keys()),
    index=list(presets.keys()).index(st.session_state.current_mode),
)

load_col, log_col = st.columns([1, 1])
with load_col:
    if st.button("Load Selected Mode", use_container_width=True):
        set_mode(st, selected_mode)
        st.success(f"Loaded mode: {selected_mode}")

with log_col:
    if st.button("Save Mode to Lighting Log", use_container_width=True):
        add_log(
            st,
            event_type="Mode Saved",
            mode_name=st.session_state.current_mode,
            settings=st.session_state.current_settings,
        )
        st.success("Lighting mode saved to log.")

settings = st.session_state.current_settings
risk_label, risk_score, risk_messages = assess_light_risk(settings)

left, right = st.columns([1.2, 1])

with left:
    st.subheader("Current Light Sources")
    st.dataframe(settings_to_dataframe(settings), use_container_width=True, hide_index=True)

with right:
    st.subheader("Safety and Workflow")
    st.write(f"**Risk label:** {risk_label}")
    st.write(f"**Risk score:** {risk_score}")

    for message in risk_messages:
        if risk_label == "High":
            st.error(message)
        elif risk_label == "Moderate":
            st.warning(message)
        else:
            st.success(message)

    st.write("**Preset note:**")
    st.write(settings.get("notes", ""))

st.subheader("Hardware-Ready Payload Preview")

payload = build_device_payload(
    mode_name=st.session_state.current_mode,
    settings=settings,
    operatory=st.session_state.active_operatory,
    dentist=st.session_state.dentist_name,
    assistant=st.session_state.assistant_name,
)

st.json(payload, expanded=False)

st.caption(
    "Use the sidebar pages for detailed procedure sequencing, light mixing, CureGuard, ShadeLock, "
    "SteriLight, device simulation, and reports."
)