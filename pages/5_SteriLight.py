import streamlit as st

from litelight_core import add_log, ensure_state, set_mode

st.set_page_config(page_title="SteriLight", page_icon="🧼", layout="wide")
ensure_state(st)

st.title("SteriLight Mode")
st.caption("Cleaning, barrier replacement, and operatory reset lighting workflow.")

if st.button("Load Cleaning and Reset Lighting Mode", use_container_width=True):
    set_mode(st, "Cleaning and Reset")
    st.success("Cleaning and Reset mode loaded.")

settings = st.session_state.current_settings

left, right = st.columns([1, 1])

with left:
    st.subheader("Turnover Checklist")

    light_handles = st.checkbox("Light handles wiped or barrier replaced")
    chair_controls = st.checkbox("Chair controls wiped")
    assistant_controls = st.checkbox("Assistant-side controls wiped")
    patient_surfaces = st.checkbox("Patient-contact surfaces reset")
    foot_pedal = st.checkbox("Foot pedal checked")
    suction_area = st.checkbox("Suction / handpiece zone checked")
    room_ready = st.checkbox("Room ready for next patient")

    checklist = {
        "light_handles": light_handles,
        "chair_controls": chair_controls,
        "assistant_controls": assistant_controls,
        "patient_surfaces": patient_surfaces,
        "foot_pedal": foot_pedal,
        "suction_area": suction_area,
        "room_ready": room_ready,
    }

with right:
    st.subheader("Lighting State")

    settings["main_dental_light"] = st.slider("Main Dental Light (%)", 0, 100, int(settings.get("main_dental_light", 85)))
    settings["assistant_fill"] = st.slider("Assistant Fill (%)", 0, 100, int(settings.get("assistant_fill", 65)))
    settings["ambient_room"] = st.slider("Ambient Room (%)", 0, 100, int(settings.get("ambient_room", 80)))
    settings["cleaning_prompt"] = True
    settings["beam"] = "Wide bright"

    completed = sum(1 for value in checklist.values() if value)
    total = len(checklist)
    st.metric("Checklist Completion", f"{completed}/{total}")

    if completed == total:
        st.success("Operatory reset checklist complete.")
    else:
        st.warning("Operatory reset checklist incomplete.")

    if st.button("Save SteriLight Turnover Log", use_container_width=True):
        add_log(
            st,
            event_type="SteriLight Turnover",
            mode_name="Cleaning and Reset",
            settings=settings,
            details=checklist,
        )
        st.success("SteriLight turnover log saved.")