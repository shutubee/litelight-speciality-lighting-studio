import time

import streamlit as st

from litelight_core import add_log, ensure_state

st.set_page_config(page_title="CureGuard", page_icon="🟦", layout="wide")
ensure_state(st)

st.title("CureGuard™")
st.caption("Curing workflow timer, eyewear confirmation, and procedure log support.")

settings = st.session_state.current_settings

left, right = st.columns([1, 1])

with left:
    st.subheader("Curing Setup")

    material = st.selectbox(
        "Material / use case",
        [
            "Composite",
            "Flowable composite",
            "Bonding agent",
            "Sealant",
            "Resin cement",
            "Other",
        ],
    )
    tooth = st.text_input("Tooth / site", "36")
    exposure_time = st.slider("Exposure time (seconds)", 5, 60, 20, step=5)
    distance_check = st.selectbox(
        "Distance check",
        ["Manual check required", "Close and perpendicular", "Difficult access", "Not recorded"],
    )

    eyewear_confirmed = st.checkbox("Eye protection confirmed for operator / assistant / patient")
    assistant_confirmed = st.checkbox("Assistant confirmation complete")
    manufacturer_ifu = st.checkbox("Manufacturer instructions checked for material and curing unit")

    repeated_exposure = st.number_input("Number of repeated exposures", min_value=1, max_value=10, value=1)

    thermal_note = st.text_area(
        "Thermal / clinical note",
        "No unusual heat concern reported during this curing step.",
    )

    if not eyewear_confirmed:
        st.warning("Eye protection is not confirmed.")
    if not manufacturer_ifu:
        st.warning("Manufacturer instructions are not confirmed.")

    if st.button("Run Simulated Cure Timer", use_container_width=True):
        progress = st.progress(0)
        status = st.empty()

        for i in range(exposure_time):
            progress.progress((i + 1) / exposure_time)
            status.write(f"Curing timer: {i + 1} / {exposure_time} seconds")
            time.sleep(0.02)

        status.success("Simulated curing timer complete.")

with right:
    st.subheader("CureGuard Status")

    status_items = {
        "Material": material,
        "Tooth / Site": tooth,
        "Exposure Time": f"{exposure_time} s",
        "Distance Check": distance_check,
        "Eye Protection": "Confirmed" if eyewear_confirmed else "Not confirmed",
        "Assistant Confirmation": "Confirmed" if assistant_confirmed else "Not confirmed",
        "Manufacturer IFU": "Checked" if manufacturer_ifu else "Not checked",
        "Repeated Exposures": repeated_exposure,
    }

    for key, value in status_items.items():
        st.write(f"**{key}:** {value}")

    cure_details = {
        "material": material,
        "tooth": tooth,
        "exposure_time_seconds": exposure_time,
        "distance_check": distance_check,
        "eyewear_confirmed": eyewear_confirmed,
        "assistant_confirmed": assistant_confirmed,
        "manufacturer_ifu_checked": manufacturer_ifu,
        "repeated_exposure_count": repeated_exposure,
        "thermal_note": thermal_note,
    }

    if st.button("Save CureGuard Log", use_container_width=True):
        add_log(
            st,
            event_type="CureGuard",
            mode_name=st.session_state.current_mode,
            settings=settings,
            details=cure_details,
        )
        st.success("CureGuard log saved.")

    st.subheader("CureGuard Record Preview")
    st.json(cure_details)