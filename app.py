"""Flora — ¿Sale plancito? 🎮

Propuesta de plancito casual con michis y onda gamer en Streamlit.
"""

import streamlit as st

from floraapp import content, music, state, steps, theme, tracker, ui

st.set_page_config(
    page_title="Flora — ¿Sale plancito? 🎮",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Registrar visita en disco (una sola vez por sesión de navegador)
is_admin = tracker.is_admin_request()
tracker.track_visit(is_admin=is_admin)

# Si se accede con ?admin o ?stats, muestra el panel privado y detiene la ejecución
if is_admin:
    tracker.render_admin_dashboard()
    st.stop()

state.init()
theme.inject(steps.dynamic_css())
st.markdown(ui.header(), unsafe_allow_html=True)
steps.render()

# Música de fondo en playlist aleatoria (sobrevive a los pasos).
music.background(content.PLAYLIST)
