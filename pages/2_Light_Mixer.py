import streamlit as st

from litelight_core import (
    add_log,
    assess_light_risk,
    build_device_payload,
    ensure_state,
    settings_to_dataframe,
)

st.set_page_config(page_title="Light Mixer", page_icon="🎚️", layout="wide")
ensure_state(st)

st.title("Light Mixer")
st.caption("Manually tune dental light sources for the active procedure mode.")

settings = st.session_state.current_settings

left, right = st.columns([1, 1])

with left:
    st.subheader("Light Source Levels")

    settings["main_dental_light"] = st.slider(
        "Main Dental Light (%)",
        0,
        100,
        int(settings.get("main_dental_light", 0)),
    )
    settings["assistant_fill"] = st.slider(
        "Assistant Fill (%)",
        0,
        100,
        int(settings.get("assistant_fill", 0)),
    )
    settings["loupe_light"] = st.slider(
        "Loupe / Headlight (%)",
        0,
        100,
        int(settings.get("loupe_light", 0)),
    )
    settings["ambient_room"] = st.slider(
        "Ambient Room Light (%)",
        0,
        100,
        int(settings.get("ambient_room", 0)),
    )
    settings["photo_light"] = st.slider(
        "Photo Light (%)",
        0,
        100,
        int(settings.get("photo_light", 0)),
    )

    st.subheader("Optical Settings")
    settings["cct_k"] = st.slider(
        "Colour Temperature (K)",
        3000,
        6500,
        int(settings.get("cct_k", 5000)),
        step=100,
    )
    settings["beam"] = st.selectbox(
        "Beam Type",
        ["Wide soft", "Medium", "Medium focused", "Focused", "Deep focused", "High stability", "Neutral calibrated", "Documentation", "Wide bright"],
        index=0,
    )

    st.subheader("Workflow Controls")
    settings["glare_control"] = st.toggle("Glare Control", bool(settings.get("glare_control", True)))
    settings["shadow_control"] = st.toggle("Shadow Control", bool(settings.get("shadow_control", True)))
    settings["curing_prompt"] = st.toggle("Curing Prompt", bool(settings.get("curing_prompt", False)))
    settings["cleaning_prompt"] = st.toggle("Cleaning Prompt", bool(settings.get("cleaning_prompt", False)))

    st.session_state.current_settings = settings

    if st.button("Save Mixer State to Log", use_container_width=True):
        add_log(
            st,
            event_type="Manual Mixer State",
            mode_name=st.session_state.current_mode,
            settings=settings,
        )
        st.success("Mixer state saved.")

with right:
    st.subheader("Live Mixer Summary")
    st.dataframe(settings_to_dataframe(settings), use_container_width=True, hide_index=True)

    risk_label, risk_score, messages = assess_light_risk(settings)
    st.write(f"### Risk: {risk_label} ({risk_score})")

    for message in messages:
        if risk_label == "High":
            st.error(message)
        elif risk_label == "Moderate":
            st.warning(message)
        else:
            st.success(message)

    st.subheader("Device Payload")
    payload = build_device_payload(
        mode_name=st.session_state.current_mode,
        settings=settings,
        operatory=st.session_state.active_operatory,
        dentist=st.session_state.dentist_name,
        assistant=st.session_state.assistant_name,
    )
    st.json(payload, expanded=False)