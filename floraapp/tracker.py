"""Módulo de rastreo y analíticas de visitas privadas guardadas en disco."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import streamlit as st

try:
    from zoneinfo import ZoneInfo
    ARG_TZ = ZoneInfo("America/Argentina/Buenos_Aires")
except Exception:
    ARG_TZ = timezone(timedelta(hours=-3))

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
VISITS_FILE = DATA_DIR / "visits.json"


def _now_str() -> str:
    return datetime.now(ARG_TZ).strftime("%Y-%m-%d %H:%M:%S")


def _load_data() -> dict:
    if not VISITS_FILE.exists():
        return {"visits": []}
    try:
        with open(VISITS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"visits": []}
            if "visits" not in data or not isinstance(data["visits"], list):
                data["visits"] = []
            return data
    except Exception:
        return {"visits": []}


def _save_data(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp_file = VISITS_FILE.with_suffix(".tmp")
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp_file.replace(VISITS_FILE)
    except Exception:
        pass


def _extract_client_info() -> dict:
    ip = None
    user_agent = None
    device = "Navegador Web"

    try:
        if hasattr(st, "context"):
            ip = getattr(st.context, "ip_address", None)
            headers = getattr(st.context, "headers", None)
            if headers:
                user_agent = headers.get("user-agent") or headers.get("User-Agent")
                if not ip:
                    fwd = headers.get("x-forwarded-for") or headers.get("X-Forwarded-For")
                    if fwd:
                        ip = fwd.split(",")[0].strip()
                    else:
                        ip = headers.get("x-real-ip") or headers.get("X-Real-Ip")
    except Exception:
        pass

    if user_agent:
        ua = user_agent.lower()
        if "iphone" in ua:
            device = "iPhone (Móvil)"
        elif "ipad" in ua:
            device = "iPad (Tablet)"
        elif "android" in ua:
            device = "Android (Móvil)"
        elif "windows" in ua:
            device = "Windows (PC)"
        elif "macintosh" in ua or "mac os" in ua:
            device = "Mac (PC)"
        elif "linux" in ua:
            device = "Linux (PC)"

    return {
        "ip": ip or "127.0.0.1",
        "user_agent": user_agent or "Desconocido",
        "device": device,
    }


def is_admin_request() -> bool:
    """Verifica si la petición actual contiene el parámetro secreto ?admin o ?stats."""
    try:
        return "admin" in st.query_params or "stats" in st.query_params
    except Exception:
        return False


def track_visit(is_admin: bool = False) -> None:
    """Registra la visita en disco si es una nueva sesión de navegador."""
    if "tracked_session_id" in st.session_state:
        return

    session_id = str(uuid.uuid4())[:8]
    st.session_state["tracked_session_id"] = session_id

    client = _extract_client_info()
    data = _load_data()

    visit_entry = {
        "session_id": session_id,
        "timestamp": _now_str(),
        "is_admin": is_admin,
        "device": client["device"],
        "ip": client["ip"],
        "user_agent": client["user_agent"],
        "said_yes": False,
        "no_attempts": 0,
        "chosen_plan": None,
        "chosen_datetime": None,
        "last_action": "Accedió al panel admin" if is_admin else "Accedió a la web",
        "last_active": _now_str(),
    }

    data["visits"].insert(0, visit_entry)
    _save_data(data)


def log_action(action: str, **kwargs) -> None:
    """Actualiza la sesión actual con la última acción o respuesta."""
    session_id = st.session_state.get("tracked_session_id")
    if not session_id:
        return

    data = _load_data()
    updated = False
    for v in data.get("visits", []):
        if v.get("session_id") == session_id:
            v["last_action"] = action
            v["last_active"] = _now_str()
            for k, val in kwargs.items():
                if val is not None:
                    v[k] = val
            updated = True
            break

    if updated:
        _save_data(data)


def clear_history() -> None:
    _save_data({"visits": []})


def render_admin_dashboard() -> None:
    """Renderiza el panel privado de administración."""
    data = _load_data()
    visits = data.get("visits", [])

    total_visits = len(visits)
    external_visits = [v for v in visits if not v.get("is_admin")]
    admin_visits = [v for v in visits if v.get("is_admin")]
    unique_ips = len(set(v.get("ip") for v in visits if v.get("ip")))

    st.markdown(
        """
        <style>
        .admin-box {
            background: #18122B;
            border: 1px solid #7c3aed;
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 20px;
            color: #f3f4f6;
            font-family: 'Nunito', sans-serif;
        }
        .admin-title {
            font-size: 22px;
            font-weight: 800;
            color: #a78bfa;
            margin-bottom: 4px;
        }
        .admin-sub {
            font-size: 13px;
            color: #9ca3af;
            margin-bottom: 4px;
        }
        .visit-card {
            background: #231942;
            border: 1px solid #4338ca;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            color: #e5e7eb;
            font-family: 'Nunito', sans-serif;
        }
        .badge-visitor {
            background: #ec4899;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }
        .badge-admin {
            background: #6366f1;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="admin-box">
            <div class="admin-title">🛡️ Panel Privado de Visitas</div>
            <div class="admin-sub">Registro de accesos y actividad guardado en disco (sólo visible para vos).</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Visitas", total_visits)
    with col2:
        st.metric("🌸 Visitas de Ella / Externas", len(external_visits))
    with col3:
        st.metric("🛡️ Visitas Admin", len(admin_visits))
    with col4:
        st.metric("IPs Únicas", unique_ips)

    st.markdown("---")

    top_col1, top_col2 = st.columns([1, 1])
    with top_col1:
        if st.button("👁️ Ver web como visitante (salir del panel)", use_container_width=True):
            st.query_params.clear()
            st.rerun()
    with top_col2:
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 Descargar log en JSON",
            data=json_str,
            file_name=f"visitas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("### 📋 Historial de Entradas")

    if not visits:
        st.info("Aún no hay visitas registradas en disco.")
    else:
        for idx, v in enumerate(visits):
            is_adm = v.get("is_admin", False)
            badge_class = "badge-admin" if is_adm else "badge-visitor"
            badge_text = "🛡️ ADMIN" if is_adm else "🌸 VISITANTE"

            detalles = []
            if v.get("said_yes"):
                detalles.append("✅ Dijo que Sí")
            if v.get("no_attempts", 0) > 0:
                detalles.append(f"❌ Intentó 'No' {v['no_attempts']} vez/veces")
            if v.get("chosen_plan"):
                detalles.append(f"🎮 Plan: {v['chosen_plan']}")
            if v.get("chosen_datetime"):
                detalles.append(f"📅 Fecha/Hora: {v['chosen_datetime']}")
            if not detalles:
                detalles.append(f"Acción: {v.get('last_action', 'Entró a la web')}")

            detalles_str = " · ".join(detalles)

            st.markdown(
                f"""
                <div class="visit-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span><strong>#{len(visits) - idx}</strong> — 🕒 <strong>{v.get('timestamp')}</strong></span>
                        <span class="{badge_class}">{badge_text}</span>
                    </div>
                    <div style="font-size:13px; color:#d1d5db; margin-bottom:4px;">
                        📱 <strong>Dispositivo:</strong> {v.get('device', 'Desconocido')} &nbsp;|&nbsp; 🌐 <strong>IP:</strong> {v.get('ip', 'N/A')}
                    </div>
                    <div style="font-size:13px; color:#a78bfa;">
                        💡 <strong>Actividad:</strong> {detalles_str}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    with st.expander("⚙️ Opciones de Mantenimiento"):
        confirma = st.checkbox("Confirmo que deseo borrar todo el historial de visitas guardado.")
        if st.button("🗑️ Limpiar historial de visitas", type="secondary", disabled=not confirma):
            clear_history()
            st.success("Historial borrado correctamente.")
            st.rerun()
