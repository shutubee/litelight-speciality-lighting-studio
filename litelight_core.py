from __future__ import annotations

import io
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd

PRODUCT_NAME = "Litelight™ Specialty Lighting"
PURPOSE = "Dentistry"
AUTHOR = "Pushpa Ramakrishnan"

DATA_DIR = Path(__file__).parent / "data"
PRESETS_PATH = DATA_DIR / "presets.json"


DEFAULT_PRESETS: Dict[str, Dict[str, Any]] = {
    "Patient Entry": {
        "main_dental_light": 25,
        "assistant_fill": 10,
        "loupe_light": 0,
        "ambient_room": 35,
        "photo_light": 0,
        "cct_k": 3500,
        "beam": "Wide soft",
        "curing_prompt": False,
        "glare_control": True,
        "shadow_control": False,
        "cleaning_prompt": False,
        "notes": "Soft, low-glare operatory lighting for patient entry and comfort.",
    },
    "Examination": {
        "main_dental_light": 65,
        "assistant_fill": 25,
        "loupe_light": 20,
        "ambient_room": 30,
        "photo_light": 0,
        "cct_k": 5000,
        "beam": "Medium",
        "curing_prompt": False,
        "glare_control": True,
        "shadow_control": True,
        "cleaning_prompt": False,
        "notes": "Neutral oral-cavity illumination for initial assessment.",
    },
    "Scaling": {
        "main_dental_light": 75,
        "assistant_fill": 45,
        "loupe_light": 35,
        "ambient_room": 25,
        "photo_light": 0,
        "cct_k": 5200,
        "beam": "Medium focused",
        "curing_prompt": False,
        "glare_control": True,
        "shadow_control": True,
        "cleaning_prompt": False,
        "notes": "Higher contrast with fill support for calculus, plaque, and gingival margin visibility.",
    },
    "Cavity Preparation": {
        "main_dental_light": 70,
        "assistant_fill": 35,
        "loupe_light": 45,
        "ambient_room": 20,
        "photo_light": 0,
        "cct_k": 5200,
        "beam": "Focused",
        "curing_prompt": False,
        "glare_control": True,
        "shadow_control": True,
        "cleaning_prompt": False,
        "notes": "Focused illumination for fine tooth-preparation visibility.",
    },
    "Composite Restoration": {
        "main_dental_light": 55,
        "assistant_fill": 25,
        "loupe_light": 35,
        "ambient_room": 20,
        "photo_light": 0,
        "cct_k": 4800,
        "beam": "Focused medium",
        "curing_prompt": True,
        "glare_control": True,
        "shadow_control": True,
        "cleaning_prompt": False,
        "notes": "Balanced light with CureGuard readiness for composite work.",
    },
    "Endodontics": {
        "main_dental_light": 80,
        "assistant_fill": 40,
        "loupe_light": 60,
        "ambient_room": 20,
        "photo_light": 0,
        "cct_k": 5400,
        "beam": "Deep focused",
        "curing_prompt": False,
        "glare_control": True,
        "shadow_control": True,
        "cleaning_prompt": False,
        "notes": "Deep-field visibility for root canal procedures and loupe coordination.",
    },
    "Surgery": {
        "main_dental_light": 90,
        "assistant_fill": 55,
        "loupe_light": 45,
        "ambient_room": 30,
        "photo_light": 0,
        "cct_k": 5500,
        "beam": "High stability",
        "curing_prompt": False,
        "glare_control": True,
        "shadow_control": True,
        "cleaning_prompt": False,
        "notes": "High-visibility mode for implant, extraction, and oral surgery workflows.",
    },
    "Shade Match": {
        "main_dental_light": 45,
        "assistant_fill": 20,
        "loupe_light": 0,
        "ambient_room": 35,
        "photo_light": 40,
        "cct_k": 5500,
        "beam": "Neutral calibrated",
        "curing_prompt": False,
        "glare_control": True,
        "shadow_control": False,
        "cleaning_prompt": False,
        "notes": "Colour-stable setting for crowns, veneers, whitening, and shade comparison.",
    },
    "Photography": {
        "main_dental_light": 35,
        "assistant_fill": 20,
        "loupe_light": 0,
        "ambient_room": 25,
        "photo_light": 75,
        "cct_k": 5600,
        "beam": "Documentation",
        "curing_prompt": False,
        "glare_control": True,
        "shadow_control": False,
        "cleaning_prompt": False,
        "notes": "Repeatable lighting for before-after and clinical documentation.",
    },
    "Cleaning and Reset": {
        "main_dental_light": 85,
        "assistant_fill": 65,
        "loupe_light": 0,
        "ambient_room": 80,
        "photo_light": 0,
        "cct_k": 5000,
        "beam": "Wide bright",
        "curing_prompt": False,
        "glare_control": False,
        "shadow_control": False,
        "cleaning_prompt": True,
        "notes": "Bright broad light for surface inspection, barrier replacement, and room reset.",
    },
}


def get_presets() -> Dict[str, Dict[str, Any]]:
    if PRESETS_PATH.exists():
        with PRESETS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return deepcopy(DEFAULT_PRESETS)


def ensure_state(st_module: Any) -> None:
    presets = get_presets()

    if "current_mode" not in st_module.session_state:
        st_module.session_state.current_mode = "Examination"

    if "current_settings" not in st_module.session_state:
        st_module.session_state.current_settings = deepcopy(presets["Examination"])

    if "lighting_log" not in st_module.session_state:
        st_module.session_state.lighting_log = []

    if "device_online" not in st_module.session_state:
        st_module.session_state.device_online = False

    if "active_operatory" not in st_module.session_state:
        st_module.session_state.active_operatory = "Operatory 1"

    if "dentist_name" not in st_module.session_state:
        st_module.session_state.dentist_name = "Dr. _______"

    if "assistant_name" not in st_module.session_state:
        st_module.session_state.assistant_name = "Assistant _______"


def set_mode(st_module: Any, mode_name: str) -> None:
    presets = get_presets()
    st_module.session_state.current_mode = mode_name
    st_module.session_state.current_settings = deepcopy(presets[mode_name])


def settings_to_dataframe(settings: Dict[str, Any]) -> pd.DataFrame:
    rows = [
        ("Main Dental Light", settings.get("main_dental_light", 0), "Primary oral-cavity source"),
        ("Assistant Fill", settings.get("assistant_fill", 0), "Shadow reduction support"),
        ("Loupe Light", settings.get("loupe_light", 0), "Dentist headlight / loupe channel"),
        ("Ambient Room", settings.get("ambient_room", 0), "Operatory background lighting"),
        ("Photo Light", settings.get("photo_light", 0), "Clinical documentation source"),
    ]
    return pd.DataFrame(rows, columns=["Light Source", "Level %", "Purpose"])


def assess_light_risk(settings: Dict[str, Any]) -> Tuple[str, int, List[str]]:
    score = 0
    messages: List[str] = []

    main = int(settings.get("main_dental_light", 0))
    fill = int(settings.get("assistant_fill", 0))
    loupe = int(settings.get("loupe_light", 0))
    photo = int(settings.get("photo_light", 0))
    glare = bool(settings.get("glare_control", False))
    shadow = bool(settings.get("shadow_control", False))

    if main >= 85:
        score += 2
        messages.append("Main light is high; confirm patient-eye comfort and chair angle.")
    elif main >= 70:
        score += 1
        messages.append("Main light is elevated; keep glare control active.")

    if loupe >= 70:
        score += 1
        messages.append("Loupe light is high; confirm it is not fighting the main source.")

    if fill < 20 and main >= 65:
        score += 1
        messages.append("Low fill with high main light may increase instrument shadows.")

    if photo >= 70 and main >= 65:
        score += 1
        messages.append("Photo and main lights are both high; check reflections and washout.")

    if not glare and main >= 60:
        score += 2
        messages.append("Glare control is off while main brightness is clinically significant.")

    if not shadow and fill < 25 and main >= 60:
        score += 1
        messages.append("Shadow control is off; assistant fill may be insufficient.")

    if score <= 1:
        return "Low", score, messages or ["Lighting state is within normal workflow range."]
    if score <= 3:
        return "Moderate", score, messages
    return "High", score, messages


def build_device_payload(
    mode_name: str,
    settings: Dict[str, Any],
    operatory: str,
    dentist: str,
    assistant: str,
) -> Dict[str, Any]:
    risk_label, risk_score, risk_messages = assess_light_risk(settings)

    return {
        "product": PRODUCT_NAME,
        "purpose": PURPOSE,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "operatory": operatory,
        "dentist": dentist,
        "assistant": assistant,
        "mode": mode_name,
        "lights": {
            "main_dental_light": {
                "level_percent": settings.get("main_dental_light", 0),
                "cct_k": settings.get("cct_k", 5000),
                "beam": settings.get("beam", "Medium"),
            },
            "assistant_fill": {"level_percent": settings.get("assistant_fill", 0)},
            "loupe_light": {"level_percent": settings.get("loupe_light", 0)},
            "ambient_room": {"level_percent": settings.get("ambient_room", 0)},
            "photo_light": {"level_percent": settings.get("photo_light", 0)},
        },
        "workflow": {
            "curing_prompt": settings.get("curing_prompt", False),
            "glare_control": settings.get("glare_control", False),
            "shadow_control": settings.get("shadow_control", False),
            "cleaning_prompt": settings.get("cleaning_prompt", False),
        },
        "risk": {
            "label": risk_label,
            "score": risk_score,
            "messages": risk_messages,
        },
        "notes": settings.get("notes", ""),
    }


def add_log(
    st_module: Any,
    event_type: str,
    mode_name: str,
    settings: Dict[str, Any],
    details: Dict[str, Any] | None = None,
) -> None:
    risk_label, risk_score, _ = assess_light_risk(settings)
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "operatory": st_module.session_state.active_operatory,
        "dentist": st_module.session_state.dentist_name,
        "assistant": st_module.session_state.assistant_name,
        "mode": mode_name,
        "main_dental_light": settings.get("main_dental_light", 0),
        "assistant_fill": settings.get("assistant_fill", 0),
        "loupe_light": settings.get("loupe_light", 0),
        "ambient_room": settings.get("ambient_room", 0),
        "photo_light": settings.get("photo_light", 0),
        "cct_k": settings.get("cct_k", 0),
        "beam": settings.get("beam", ""),
        "risk_label": risk_label,
        "risk_score": risk_score,
        "details": json.dumps(details or {}, ensure_ascii=False),
    }
    st_module.session_state.lighting_log.append(entry)


def log_to_dataframe(log: List[Dict[str, Any]]) -> pd.DataFrame:
    if not log:
        return pd.DataFrame()
    return pd.DataFrame(log)


def make_csv_bytes(log: List[Dict[str, Any]]) -> bytes:
    df = log_to_dataframe(log)
    return df.to_csv(index=False).encode("utf-8")


def make_json_bytes(log: List[Dict[str, Any]]) -> bytes:
    return json.dumps(log, indent=2, ensure_ascii=False).encode("utf-8")


def make_pdf_bytes(log: List[Dict[str, Any]], title: str = "Litelight Lighting Log") -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{PRODUCT_NAME}</b>", styles["Title"]))
    story.append(Paragraph(f"Purpose: {PURPOSE}", styles["Normal"]))
    story.append(Paragraph(f"Author: {AUTHOR}", styles["Normal"]))
    story.append(Paragraph(title, styles["Heading2"]))
    story.append(Spacer(1, 12))

    if not log:
        story.append(Paragraph("No lighting log entries available.", styles["Normal"]))
    else:
        rows = [["Time", "Event", "Mode", "Main", "Fill", "CCT", "Risk"]]
        for entry in log[-25:]:
            rows.append([
                entry.get("timestamp", ""),
                entry.get("event_type", ""),
                entry.get("mode", ""),
                str(entry.get("main_dental_light", "")),
                str(entry.get("assistant_fill", "")),
                str(entry.get("cct_k", "")),
                entry.get("risk_label", ""),
            ])

        table = Table(rows, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E5BFF")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(table)

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "Note: This prototype is a workflow and documentation aid. It is not a regulatory submission, "
        "medical-device approval document, or replacement for manufacturer instructions.",
        styles["Normal"],
    ))

    doc.build(story)
    return buffer.getvalue()