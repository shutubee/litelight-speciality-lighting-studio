import streamlit as st

from litelight_core import build_device_payload, ensure_state

st.set_page_config(page_title="Device Simulator", page_icon="🔌", layout="wide")
ensure_state(st)

st.title("Device Simulator")
st.caption("Preview bridge commands for future lighting hardware, MQTT, BLE, Wi-Fi, or vendor API integration.")

settings = st.session_state.current_settings

left, right = st.columns([1, 1])

with left:
    st.subheader("Simulated Device Bridge")

    bridge_type = st.selectbox(
        "Bridge type",
        ["Local simulator", "MQTT bridge", "BLE bridge", "Wi-Fi bridge", "USB serial bridge", "Vendor API connector"],
    )
    device_id = st.text_input("Device ID", "LTL-DENTAL-OPERATORY-001")
    topic = st.text_input("MQTT / API topic", "litelight/dentistry/operatory-1/set")
    qos = st.selectbox("QoS / reliability level", ["Low latency", "Balanced", "Confirmed delivery"])

    st.session_state.device_online = st.toggle("Bridge online", st.session_state.device_online)

    command = {
        "bridge_type": bridge_type,
        "device_id": device_id,
        "topic": topic,
        "qos": qos,
    }

with right:
    st.subheader("Command Payload")

    payload = build_device_payload(
        mode_name=st.session_state.current_mode,
        settings=settings,
        operatory=st.session_state.active_operatory,
        dentist=st.session_state.dentist_name,
        assistant=st.session_state.assistant_name,
    )

    payload["bridge"] = command

    st.json(payload)

    if st.button("Simulate Send Command", use_container_width=True):
        if st.session_state.device_online:
            st.success("Simulated device command sent.")
        else:
            st.warning("Device bridge is offline. Command preview only.")

    st.download_button(
        "Download Payload JSON",
        data=str(payload).encode("utf-8"),
        file_name="litelight_device_payload.json",
        mime="application/json",
        use_container_width=True,
    )