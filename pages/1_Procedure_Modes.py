import streamlit as st

from litelight_core import (
    add_log,
    assess_light_risk,
    build_device_payload,
    ensure_state,
    get_presets,
    set_mode,
    settings_to_dataframe,
)

st.set_page_config(page_title="Procedure Modes", page_icon="🦷", layout="wide")
ensure_state(st)

st.title("Procedure Modes")
st.caption("Load, inspect, and sequence dentistry-specific lighting modes.")

presets = get_presets()

workflow_options = {
    "Composite Restoration Workflow": [
        "Patient Entry",
        "Examination",
        "Cavity Preparation",
        "Composite Restoration",
        "Shade Match",
        "Photography",
        "Cleaning and Reset",
    ],
    "Endodontics Workflow": [
        "Patient Entry",
        "Examination",
        "Endodontics",
        "Photography",
        "Cleaning and Reset",
    ],
    "Surgery Workflow": [
        "Patient Entry",
        "Examination",
        "Surgery",
        "Photography",
        "Cleaning and Reset",
    ],
    "Cosmetic / Shade Workflow": [
        "Patient Entry",
        "Examination",
        "Shade Match",
        "Photography",
        "Cleaning and Reset",
    ],
}

left, right = st.columns([0.9, 1.1])

with left:
    st.subheader("Mode Library")
    selected = st.selectbox("Procedure mode", list(presets.keys()))

    if st.button("Load Mode", use_container_width=True):
        set_mode(st, selected)
        st.success(f"Loaded {selected}")

    if st.button("Log Current Mode", use_container_width=True):
        add_log(
            st,
            event_type="Procedure Mode",
            mode_name=st.session_state.current_mode,
            settings=st.session_state.current_settings,
        )
        st.success("Mode logged.")

    st.divider()

    st.subheader("Workflow Sequencer")
    workflow_name = st.selectbox("Workflow template", list(workflow_options.keys()))
    workflow = workflow_options[workflow_name]

    for idx, mode in enumerate(workflow, start=1):
        cols = st.columns([0.15, 0.55, 0.3])
        cols[0].write(f"{idx}.")
        cols[1].write(mode)
        if cols[2].button("Load", key=f"load_{workflow_name}_{mode}_{idx}"):
            set_mode(st, mode)
            add_log(
                st,
                event_type=f"Workflow Step {idx}",
                mode_name=mode,
                settings=st.session_state.current_settings,
                details={"workflow": workflow_name, "step": idx},
            )
            st.rerun()

with right:
    st.subheader("Current Mode Detail")
    st.write(f"### {st.session_state.current_mode}")
    settings = st.session_state.current_settings

    st.dataframe(settings_to_dataframe(settings), use_container_width=True, hide_index=True)

    risk_label, risk_score, messages = assess_light_risk(settings)
    st.write(f"**Risk:** {risk_label} ({risk_score})")

    for message in messages:
        if risk_label == "High":
            st.error(message)
        elif risk_label == "Moderate":
            st.warning(message)
        else:
            st.success(message)

    st.write("**Notes:**")
    st.write(settings.get("notes", ""))

    st.subheader("Device Payload")
    payload = build_device_payload(
        mode_name=st.session_state.current_mode,
        settings=settings,
        operatory=st.session_state.active_operatory,
        dentist=st.session_state.dentist_name,
        assistant=st.session_state.assistant_name,
    )
    st.json(payload, expanded=False)