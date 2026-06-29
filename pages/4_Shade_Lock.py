import streamlit as st

from litelight_core import add_log, ensure_state

st.set_page_config(page_title="ShadeLock", page_icon="🎨", layout="wide")
ensure_state(st)

st.title("ShadeLock™")
st.caption("Colour-stable lighting workflow for cosmetic and restorative dentistry.")

settings = st.session_state.current_settings

left, right = st.columns([1, 1])

with left:
    st.subheader("Shade Matching Setup")

    target_cct = st.slider("Target colour temperature (K)", 4000, 6500, 5500, step=100)
    settings["cct_k"] = target_cct

    shade_system = st.selectbox(
        "Shade system",
        ["VITA Classical", "VITA 3D-Master", "Custom clinic shade tab", "Digital scanner reference", "Other"],
    )
    shade_value = st.text_input("Selected shade / note", "A2")
    grey_card = st.checkbox("Grey card / neutral reference used")
    photo_reference = st.checkbox("Photo documentation captured")
    ambient_controlled = st.checkbox("Ambient colour cast controlled")
    patient_lip_retractor = st.checkbox("Lip retractor / field visibility acceptable")

    settings["main_dental_light"] = st.slider("Main Dental Light (%)", 0, 100, int(settings.get("main_dental_light", 45)))
    settings["photo_light"] = st.slider("Photo Light (%)", 0, 100, int(settings.get("photo_light", 40)))
    settings["ambient_room"] = st.slider("Ambient Room (%)", 0, 100, int(settings.get("ambient_room", 35)))
    settings["beam"] = "Neutral calibrated"

    st.session_state.current_settings = settings

with right:
    st.subheader("ShadeLock Status")

    if target_cct < 5000:
        st.warning("Shade matching usually benefits from a neutral daylight-like condition. Confirm clinic preference.")
    else:
        st.success("Target CCT is within a neutral shade-matching range.")

    if not ambient_controlled:
        st.warning("Ambient colour cast is not confirmed as controlled.")

    if not grey_card:
        st.info("Grey card/reference not confirmed. Add one for repeatable documentation.")

    shade_details = {
        "target_cct_k": target_cct,
        "shade_system": shade_system,
        "shade_value": shade_value,
        "grey_card_used": grey_card,
        "photo_reference_captured": photo_reference,
        "ambient_colour_cast_controlled": ambient_controlled,
        "field_visibility_acceptable": patient_lip_retractor,
    }

    st.json(shade_details)

    if st.button("Save ShadeLock Log", use_container_width=True):
        add_log(
            st,
            event_type="ShadeLock",
            mode_name="Shade Match",
            settings=settings,
            details=shade_details,
        )
        st.success("ShadeLock log saved.")