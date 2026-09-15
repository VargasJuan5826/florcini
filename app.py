"""Flora — ¿Sale plancito? 🎮

Propuesta de plancito casual con michis y onda gamer en Streamlit.
"""

import streamlit as st

from floraapp import content, music, state, steps, theme, ui

st.set_page_config(
    page_title="Flora — ¿Sale plancito? 🎮",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

state.init()
theme.inject(steps.dynamic_css())
st.markdown(ui.header(), unsafe_allow_html=True)
steps.render()

# Música de fondo (arranca en el primer click, sobrevive a los pasos). Va al final para no
# afectar el layout; el player real se inyecta en el documento padre.
music.background(content.MUSIC_VIDEO_ID, content.MUSIC_START_SECONDS)
