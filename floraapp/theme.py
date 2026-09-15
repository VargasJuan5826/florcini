"""CSS de la app.

Los tokens, keyframes y medidas son los mismos que `app/globals.css` y los estilos
inline del original en Next.js. El resto son los reset necesarios para que los widgets
de Streamlit se vean exactamente como los `<button>` originales.

Convenciones:
  * cada widget lleva `key="flora_..."` y Streamlit publica ese key como clase
    `st-key-flora_...`, así que los selectores usan `[class*="st-key-flora_opt_"]` para
    estilar familias completas de widgets;
  * los bloques de HTML propio se envuelven en `.flora` para ganarle en especificidad a
    los estilos del markdown de Streamlit.
"""

from __future__ import annotations

import streamlit as st

from . import content

TOKENS = """
:root {
  --bg: #f7f3ff;
  --card: #ffffff;
  --primary: #7c3aed;
  --primary-light: #ede9fe;
  --primary-dark: #5b21b6;
  --accent: #ec4899;
  --accent-light: #fce7f3;
  --green: #10b981;
  --green-light: #d1fae5;
  --text: #1e1b4b;
  --text-muted: #6b7280;
  --border: #e5e7eb;
  --shadow: 0 4px 24px rgba(124,58,237,0.12);
  --shadow-lg: 0 8px 40px rgba(124,58,237,0.18);
  --radius: 20px;
  --radius-sm: 12px;
  --mono: 'Fira Code', monospace;
  --sans: 'Nunito', sans-serif;
}
@media (max-width: 480px) {
  :root { --radius: 16px; --radius-sm: 10px; }
}
"""

KEYFRAMES = """
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes fadeDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.08); } }
@keyframes pop { from { opacity: 0; scale: 0.8; } to { opacity: 1; scale: 1; } }
@keyframes rain { from { top: -50px; opacity: 1; } to { top: 110vh; opacity: 0; } }
@keyframes fillExp { from { width: var(--prev-w, 35%); } to { width: var(--curr-w, 85%); } }
@keyframes popBadge { 0% { transform: translateY(-8px) scale(0.9); opacity: 0; } 50% { transform: translateY(0) scale(1.06); opacity: 1; } 100% { transform: translateY(0) scale(1); opacity: 1; } }
"""

SHELL = """
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stActionButton"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stBottomBlockContainer"],
[data-testid="stAppDeployButton"],
#MainMenu, footer, .stAppDeployButton,
/* Badges que inyecta Streamlit Community Cloud en el deploy (link al repo de GitHub,
   "Fork", avatar del dueño y el badge "Hosted with Streamlit"). No aparecen en local. */
[class*="viewerBadge"],
[class*="_profileContainer"],
[class*="_viewerBadge"],
a[href*="streamlit.io/cloud"],
a[href*="share.streamlit.io"] { display: none !important; }

.stApp, [data-testid="stAppViewContainer"] {
  background-color: var(--bg);
  background-image:
    radial-gradient(circle at 20% 20%, rgba(124,58,237,0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(236,72,153,0.06) 0%, transparent 50%);
  background-attachment: fixed;
  font-family: var(--sans);
  color: var(--text);
}
@media (max-width: 480px) {
  .stApp, [data-testid="stAppViewContainer"] {
    background-image:
      radial-gradient(circle at 20% 10%, rgba(124,58,237,0.06) 0%, transparent 40%),
      radial-gradient(circle at 80% 90%, rgba(236,72,153,0.04) 0%, transparent 40%);
  }
}

/* El original mide 560px y queda centrado vertical y horizontalmente. */
[data-testid="stMainBlockContainer"] {
  max-width: 560px !important;
  width: 100% !important;
  padding: 16px 12px !important;
  margin: 0 auto !important;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
/* El centrado va con `margin: auto` y no con `justify-content`: cuando el paso es más
   alto que la ventana (el calendario abierto, por ejemplo) los márgenes automáticos
   colapsan a 0 y el contenido sigue siendo alcanzable en vez de recortarse. */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
  flex: 0 0 auto;
  margin-top: auto;
  margin-bottom: auto;
}

/* Sin gaps automáticos: el espaciado lo dan los márgenes del diseño original. */
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stHorizontalBlock"] { gap: 0 !important; align-items: center; flex-wrap: nowrap !important; }
/* Streamlit apila las columnas cuando la ventana es angosta; acá las filas (calendario,
   minutos, presets) tienen que mantenerse horizontales siempre. */
[data-testid="stColumn"] { min-width: 0 !important; }
[data-testid="stLayoutWrapper"] { width: 100%; }
/* Streamlit compensa el margen de sus <p> con un margin-bottom negativo en el contenedor
   de markdown. Este port no usa <p>, así que ese -16px se comería el espaciado. */
[data-testid="stMarkdown"], [data-testid="stMarkdownContainer"] { width: 100%; }
[data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }
[data-testid="stMarkdownContainer"] p { margin: 0; }
[data-testid="stIFrame"] { display: block; border: 0; color-scheme: normal; }
.flora, .flora * { box-sizing: border-box; }
/* `globals.css` del original aplica esto a TODAS las imágenes del documento, no sólo a
   las propias. Importa replicarlo así: html2canvas mide la línea base de cada fuente con
   una sonda que incluye un <img>, y si ese <img> no es `block` el texto del PDF sale
   corrido 3px. */
img { max-width: 100%; display: block; }
/* Streamlit fuerza `object-fit: scale-down`; el original usa el default del navegador,
   que sí deforma la imagen del corgi a 90x120. */
.flora img { object-fit: contain; }

/* El original declara 'Nunito'/'Fira Code' sin cargarlas: cae en las genéricas del
   sistema. Se replica el mismo stack para obtener idéntico renderizado, y se neutraliza
   la tipografía propia de Streamlit. */
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] * { font-family: var(--sans); }
.stButton > button, .stButton > button * { font-family: var(--sans) !important; }
/* `body` vuelve al `normal` del navegador, como en el original. Además de la vista, esto
   importa para el PDF: html2canvas calcula la línea base con una sonda que hereda el
   line-height del body, y con el de Streamlit el texto salía 3px más arriba. */
body { line-height: normal; }
.flora { line-height: normal; }
/* El <body> del original mide 16px: fija el strut de las líneas y lo que heredan los
   elementos que no declaran tamaño. */
.flora { font-size: 16px; }
"""

BUTTON_BASE = """
.stButton > button {
  font-family: var(--sans);
  min-height: 0 !important;
  line-height: normal;
  transition: all 0.2s ease;
  box-shadow: none;
  cursor: pointer;
}
.stButton > button:focus, .stButton > button:focus-visible, .stButton > button:active {
  outline: none !important;
}
/* La etiqueta viaja dentro de div > span > markdown > p: que todo herede del <button>
   y que el <p> no aporte el margen del markdown. */
.stButton > button > div,
.stButton > button span,
.stButton > button [data-testid="stMarkdownContainer"],
.stButton > button p {
  font-family: inherit !important;
  font-size: inherit !important;
  font-weight: inherit !important;
  color: inherit !important;
  line-height: inherit !important;
  letter-spacing: inherit !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* .btn-next del original: el botón degradado de ancho completo. */
.st-key-flora_start .stButton > button,
.st-key-flora_confirm_date .stButton > button,
[class*="st-key-flora_next_"] .stButton > button {
  width: 100%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  padding: 12px 20px;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 12px rgba(124,58,237,0.3);
  white-space: normal;
}
.st-key-flora_start .stButton > button:hover,
.st-key-flora_confirm_date .stButton > button:hover,
[class*="st-key-flora_next_"] .stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124,58,237,0.4);
  color: #fff;
  border: none;
}
.st-key-flora_start .stButton > button { padding: 14px 20px; font-size: 14px; }
.st-key-flora_confirm_date { margin-top: 16px; }
[class*="st-key-flora_next_"] { margin-top: 12px; }
"""

BLOCKS = """
.flora-header { text-align: center; margin-bottom: 20px; animation: fadeDown .6s ease; }
.flora .flora-title { font-size: 24px; font-weight: 900; line-height: 1.2; margin: 0; padding: 0;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.flora .flora-sub { font-family: var(--mono); font-size: 11px; color: var(--text-muted);
  margin-top: 4px; }

/* HUD Rango Gamer */
.gamer-rank-card {
  display: flex; align-items: center; gap: 12px;
  background: #ffffff; border: 2px solid #ede9fe; border-radius: 16px;
  padding: 10px 16px; max-width: 380px; margin: 14px auto 0 auto;
  box-shadow: 0 4px 16px rgba(124,58,237,0.10); text-align: left;
}
.rank-badge-wrap {
  width: 44px; height: 44px; border-radius: 10px; overflow: hidden;
  background: #1e1b4b; border: 2px solid #7c3aed; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 8px rgba(124,58,237,0.3);
}
.rank-badge-wrap img { width: 100%; height: 100%; object-fit: cover; }
.rank-details { flex: 1; min-width: 0; }
.rank-header-line { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 4px; }
.rank-title-label { font-family: var(--mono); font-size: 11px; font-weight: 800; color: #7c3aed; text-transform: uppercase; letter-spacing: 0.5px; }
.rank-name-value { font-family: var(--sans); font-size: 14px; font-weight: 900; color: #1e1b4b; margin-left: 6px; }
.rank-bar-bg { height: 8px; background: #ede9fe; border-radius: 999px; overflow: hidden; margin-bottom: 3px; }
.rank-bar-fill { height: 100%; background: linear-gradient(90deg, #a78bfa, #7c3aed); border-radius: 999px; transition: width 0.4s ease; }
.rank-bar-fill.animated-fill {
  animation: fillExp 1.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
.rank-percent-label { font-family: var(--mono); font-size: 10px; color: #6b7280; font-weight: 700; text-align: right; }

.exp-levelup-badge {
  display: inline-block;
  margin-top: 10px;
  padding: 6px 14px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #ffffff;
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 800;
  border-radius: 20px;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
  animation: popBadge 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  letter-spacing: 0.5px;
}

.flora-step { animation: slideUp .4s cubic-bezier(.34,1.56,.64,1); }

.flora .plea-card { background: var(--primary-light); border: 2px solid rgba(124,58,237,0.2);
  border-radius: var(--radius); padding: 14px 16px; display: flex; gap: 14px;
  align-items: center; margin-bottom: 16px; }
.flora .plea-card img { width: 72px; height: 72px; border-radius: 12px; flex-shrink: 0; object-fit: cover; }
.flora .plea-text { font-size: 15px; font-weight: 800; color: var(--primary-dark); line-height: 1.4; }
.flora .plea-note { display: block; font-size: 11px; font-family: var(--mono);
  color: var(--primary); opacity: .8; font-weight: 400; margin-top: 4px; }

.flora .q-card { background: var(--card); border-radius: var(--radius); box-shadow: var(--shadow);
  padding: 16px; margin-bottom: 12px; border: 1px solid var(--border); }
.flora .q-tag { font-family: var(--mono); font-size: 10px; background: var(--primary-light);
  color: var(--primary); padding: 3px 8px; border-radius: 100px; display: inline-block;
  margin-bottom: 8px; font-weight: 500; }
.flora .q-text { font-size: 15px; font-weight: 800; color: var(--text); line-height: 1.4; }

.flora .flora-progress-label { font-family: var(--mono); font-size: 10px; color: var(--text-muted);
  margin-bottom: 6px; display: block; }
.flora .flora-progress-wrap { background: var(--border); border-radius: 100px; height: 5px;
  margin-bottom: 16px; overflow: hidden; }
.flora .flora-progress-fill { height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent));
  border-radius: 100px; transition: width .5s cubic-bezier(.34,1.56,.64,1); }

/* Contenedor uniforme para todas las opciones: fija el alto de la sección para que no salte,
   y muestra la imagen completa sin recortar (object-fit: contain). */
.flora .flora-qhead-fixed {
  width: 100%;
  max-width: 440px;
  height: 280px;
  margin: 0 auto 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
}
.flora .fixed-option-img {
  max-width: 100%;
  max-height: 280px;
  width: auto;
  height: auto;
  object-fit: contain !important;
  border-radius: 14px;
  box-shadow: 0 4px 16px rgba(124, 58, 237, 0.12);
  display: block;
}

.flora .err-msg { font-family: var(--mono); font-size: 10px; color: #dc2626; background: #fef2f2;
  border: 1px solid #fecaca; border-radius: 6px; padding: 6px 10px; margin-top: 8px; }

/* La tarjeta del PDF: fuera de pantalla, sólo existe para que html2canvas la fotografíe
   (ver floraapp/pdf.py). */
.flora #pdf-confirmation {
  position: absolute; left: -9999px; top: 0; width: 148mm;
  background: #fff; font-family: var(--sans);
}

.flora-rain { position: relative; }
.flora .float-cat { position: fixed; height: 90px; width: auto; border-radius: 10px; pointer-events: none;
  animation-name: rain; animation-timing-function: linear; animation-fill-mode: forwards;
  z-index: 9999; top: -120px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
@media (max-width: 480px) { .flora .float-cat { height: 65px; } }
"""

CARDS = """
/* Los pasos 1 y 2 tienen widgets dentro de la tarjeta: la tarjeta es un container. */
/* Sólo el markdown propio se centra; la etiqueta de los botones no (el campo de fecha
   lleva su texto a la izquierda y el emoji a la derecha). */
.st-key-flora_card1 [data-testid="stMarkdown"] [data-testid="stMarkdownContainer"],
.st-key-flora_card2 [data-testid="stMarkdown"] [data-testid="stMarkdownContainer"] { text-align: center; }
[data-testid="stVerticalBlock"].st-key-flora_card1,
[data-testid="stVerticalBlock"].st-key-flora_card2 {
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  padding: 16px;
  margin-bottom: 16px;
  text-align: center;
}
"""

STEP1 = """
.flora .step1-imgs { display: flex; justify-content: center; align-items: center; margin-bottom: 14px; }
.flora .step1-imgs img { max-width: 440px; max-height: 380px; width: auto; height: auto;
  object-fit: contain !important; border-radius: 16px;
  box-shadow: 0 8px 24px rgba(124,58,237,0.20); animation: float 3s ease-in-out infinite; }
.flora .step1-q { font-size: 18px; font-weight: 800; color: var(--text); line-height: 1.4;
  margin-bottom: 16px; text-align: center; }

/* Fila Sí/No: el container es el marco de referencia del botón que escapa. */
[data-testid="stVerticalBlock"].st-key-flora_yesno {
  position: relative;
  flex-direction: row !important;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 12px !important;
  min-height: 70px;
  padding: 8px 0;
}
.st-key-flora_si .stButton > button {
  font-size: 16px;
  padding: 12px 32px;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  border: none;
  font-weight: 800;
  box-shadow: 0 8px 20px rgba(124,58,237,0.24);
  transition: transform .2s ease, box-shadow .2s ease, all .2s ease;
  white-space: nowrap;
}
.st-key-flora_si .stButton > button:hover { transform: translateY(-2px) scale(1.03); color: #fff; }
.st-key-flora_no .stButton > button {
  font-size: 12px;
  padding: 10px 20px;
  border-radius: 999px;
  background: linear-gradient(135deg, #ffd5d5, #ff9292);
  color: #fff;
  border: 2px solid rgba(255,255,255,0.45);
  font-weight: 600;
  box-shadow: 0 8px 16px rgba(75,85,99,0.18);
  transition: transform .2s ease, all .2s ease;
  white-space: nowrap;
}
.st-key-flora_no .stButton > button:hover { color: #fff; }
.flora .flora-no-msg { margin-top: 10px; font-family: var(--mono); font-size: 11px;
  color: var(--primary); text-align: center; }
.flora .flora-card-foot { height: 0; }
"""

STEP2 = """
.flora .step2-imgs { display: flex; justify-content: center; margin-bottom: 12px; }
.flora .step2-imgs img { max-width: 220px; width: 75%; height: auto; border-radius: 14px;
  box-shadow: 0 4px 14px rgba(124,58,237,0.15); animation: pulse 2.5s ease-in-out infinite; }
.flora .re-tip { font-family: var(--mono); font-size: 11px; color: var(--primary-dark);
  background: var(--primary-light); padding: 6px 12px; border-radius: 8px; margin-top: 8px;
  margin-bottom: 10px; display: inline-block; font-weight: 700; border: 1px solid rgba(124,58,237,0.2); }
/* El tag de agenda.sync separa 10px; el de las preguntas, 8px. */
.flora .q-tag-agenda { margin-bottom: 10px; }
.flora .step2-q { font-size: 16px; font-weight: 800; color: var(--text); line-height: 1.4;
  margin-top: 8px; margin-bottom: 12px; }
.flora .picker-label { font-family: var(--mono); font-size: 11px; color: var(--text-muted);
  text-align: left; margin-bottom: 6px; }
.st-key-flora_field_date { margin-bottom: 16px; }

[class*="st-key-flora_field_"] .stButton > button > div {
  flex: 1 1 auto; justify-content: flex-start; text-align: left;
}
[class*="st-key-flora_field_"] .stButton > button {
  width: 100%;
  padding: 14px 16px;
  background: var(--bg);
  border: 2px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 15px;
  font-weight: 700;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: none;
  white-space: normal;
}
.st-key-flora_field_date .stButton > button::after { content: "📅"; font-size: 18px; }
.st-key-flora_field_time .stButton > button::after { content: "⏰"; font-size: 18px; }

/* Paneles emergentes de fecha y hora */
[data-testid="stVerticalBlock"].st-key-flora_cal,
[data-testid="stVerticalBlock"].st-key-flora_clock {
  margin-top: 16px;
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
}
[data-testid="stVerticalBlock"].st-key-flora_cal { border: 2px solid var(--primary); padding: 16px; }
[data-testid="stVerticalBlock"].st-key-flora_clock { border: 2px solid var(--accent); padding: 20px; }

[data-testid="stVerticalBlock"].st-key-flora_cal_head {
  flex-direction: row !important;
  justify-content: space-between;
  align-items: center;
}
.st-key-flora_cal_head [data-testid="stElementContainer"] { width: auto; flex: 0 0 auto; }
.st-key-flora_cal_head [data-testid="stMarkdown"] { flex: 1; }
[class*="st-key-flora_calnav_"] .stButton > button {
  width: 36px; height: 36px; min-height: 36px; padding: 0; border-radius: 50%;
  background: var(--primary-light); border: none; font-size: 16px; color: var(--text);
  display: flex; align-items: center; justify-content: center;
}

.flora .flora-cal-month { font-weight: 800; font-size: 14px; color: var(--primary-dark);
  text-align: center; }
.st-key-flora_cal_head { margin-bottom: 12px; }
.flora .flora-cal-week { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px;
  margin-bottom: 8px; }
.flora .flora-cal-week div { text-align: center; font-size: 10px; font-weight: 700;
  color: var(--text-muted); padding: 4px 0; }
/* Las filas del calendario separan 4px; el -4px del contenedor descuenta la última. */
.st-key-flora_cal_grid { margin-bottom: -4px; }
.st-key-flora_cal_grid [data-testid="stHorizontalBlock"] { gap: 4px !important; margin-bottom: 4px; }
.st-key-flora_cal_grid [data-testid="stColumn"] { min-width: 0 !important; }
[class*="st-key-flora_day_"] { display: flex; justify-content: center; }
[class*="st-key-flora_day_"] .stButton > button {
  width: 32px; height: 32px; min-height: 32px; padding: 0; border-radius: 50%;
  border: none; background: transparent; color: var(--text);
  font-size: 12px; font-weight: 600; display: flex; align-items: center; justify-content: center;
}
[class*="st-key-flora_day_"] .stButton > button:hover { background: var(--primary-light);
  color: var(--primary-dark); }
[class*="st-key-flora_day_"] .stButton > button:disabled {
  background: var(--bg); color: var(--text-muted); opacity: .4; cursor: not-allowed; border: none;
}
.flora .flora-day-empty { height: 32px; }
.st-key-flora_cal_done, .st-key-flora_time_done { margin-top: 12px; }
.st-key-flora_cal_done .stButton > button, .st-key-flora_time_done .stButton > button {
  width: 100%; padding: 10px; background: var(--primary); color: #fff; border: none;
  border-radius: var(--radius-sm); font-weight: 700; font-size: 13px;
}
.st-key-flora_time_done .stButton > button { background: var(--accent); }

[data-testid="stVerticalBlock"].st-key-flora_clock_row {
  flex-direction: row !important;
  justify-content: center;
  align-items: center;
  gap: 8px !important;
}
.st-key-flora_clock_row [data-testid="stElementContainer"] { width: auto; flex: 0 0 auto; }
[class*="st-key-flora_clocknav_"] .stButton > button {
  width: 40px; height: 40px; min-height: 40px; padding: 0; border-radius: 50%;
  background: var(--accent-light); border: none; font-size: 18px; color: var(--text);
  display: flex; align-items: center; justify-content: center;
}

.flora .flora-clock-face { display: flex; align-items: baseline; gap: 4px; justify-content: center; }
.flora .flora-clock-face .hh, .flora .flora-clock-face .mm { font-size: 36px; font-weight: 900;
  color: var(--primary-dark); }
.flora .flora-clock-face .sep { font-size: 24px; color: var(--accent); }
.st-key-flora_clock_row { margin-bottom: 16px; }
.st-key-flora_minutes { margin-bottom: 16px; }
.st-key-flora_minutes [data-testid="stHorizontalBlock"] { gap: 8px !important; }
[class*="st-key-flora_min_"] .stButton > button {
  width: 100%; padding: 8px; border-radius: var(--radius-sm); border: 2px solid var(--border);
  background: transparent; color: var(--text); font-weight: 700; font-size: 13px;
}
"""

OPTIONS = """
.st-key-flora_options { margin-top: 0; }
[class*="st-key-flora_opt_"] { margin-bottom: 8px; }
[class*="st-key-flora_opt_"] .stButton > button {
  width: 100%;
  background: var(--bg);
  border: 2px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-family: var(--sans);
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 8px;
  text-align: left;
  line-height: 1.3;
  white-space: normal;
  word-break: break-word;
  box-shadow: none;
}
[class*="st-key-flora_opt_"] .stButton > button:hover { border-color: var(--primary); }
[class*="st-key-flora_opt_"] .stButton > button::before {
  width: 22px; height: 22px; background: var(--border); border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--mono); font-size: 10px; font-weight: 600; color: var(--text);
  flex-shrink: 0;
}
[class*="st-key-flora_opt_"] .stButton > button > div {
  flex: 1; text-align: left; min-width: 0; display: block;
}
"""

SUMMARY = """
.flora .summary-header { text-align: center; margin-bottom: 16px; }
.flora .summary-header img { margin: 0 auto 10px; width: 140px; height: auto; border-radius: 14px;
  box-shadow: 0 4px 16px rgba(124,58,237,0.15); animation: pulse 2s ease-in-out infinite; }
.flora .summary-title { font-size: 22px; font-weight: 900;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.flora .summary-note { font-family: var(--mono); font-size: 11px; color: var(--text-muted);
  margin-top: 4px; }
.flora .summary-table { background: var(--card); border-radius: var(--radius);
  box-shadow: var(--shadow); overflow: hidden; border: 1px solid var(--border);
  margin-bottom: 12px; font-size: 11px; }
.flora .summary-row { display: flex; align-items: center; padding: 10px 12px; gap: 8px;
  border-bottom: 1px solid var(--border); }
.flora .summary-row.alt { background: var(--bg); }
.flora .summary-row:last-child { border-bottom: none; }
.flora .s-icon { font-size: 16px; flex-shrink: 0; width: 24px; text-align: center; }
.flora .s-label { font-family: var(--mono); font-size: 10px; color: var(--text-muted); flex-shrink: 0; }
.flora .s-value { font-weight: 700; font-size: 12px; color: var(--text); flex: 1;
  word-break: break-word; }

.flora .final-card { border: 2px solid var(--primary); text-align: center; padding: 16px;
  border-radius: var(--radius); background: var(--card); box-shadow: var(--shadow); }
.flora .final-card .q-text { font-size: 18px; line-height: 1.4; margin: 0; }
.flora .final-note { font-family: var(--mono); font-size: 10px; color: var(--text-muted);
  margin-top: 6px; }

.st-key-flora_celebrate { margin-top: 12px; }
.st-key-flora_celebrate .stButton > button {
  width: 100%; background: linear-gradient(135deg, var(--primary), var(--primary-dark)); color: #fff;
  border: none; border-radius: var(--radius-sm); padding: 14px 20px; font-size: 13px;
  font-weight: 800; letter-spacing: .5px; box-shadow: 0 4px 14px rgba(124,58,237,0.3);
  white-space: normal;
}
.st-key-flora_celebrate .stButton > button:hover { transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124,58,237,0.4); color: #fff; }

.flora .finale { text-align: center; padding: 16px; background: var(--green-light);
  border: 2px solid rgba(16,185,129,0.3); border-radius: var(--radius);
  animation: pop .5s cubic-bezier(.34,1.56,.64,1); margin-top: 12px; }
.flora .finale-imgs { display: flex; justify-content: center; align-items: center; gap: 8px;
  margin-bottom: 10px; }
.flora .finale-imgs img { object-fit: cover; border-radius: 12px; }
.flora .finale-imgs img:nth-child(odd) { width: 60px; height: 60px; }
.flora .finale-imgs img:nth-child(2) { width: 90px; height: 90px; }
.flora .finale-title { font-size: 18px; font-weight: 900; color: var(--green); margin-bottom: 6px; }
.flora .finale-note { font-family: var(--mono); font-size: 10px; color: #065f46; line-height: 1.5; }
"""


def _letters_css() -> str:
    """Badge A/B/C/D/… de cada opción (el original lo dibuja con un <span>)."""
    return "\n".join(
        f'.st-key-flora_opt_{question["id"]}_{index} .stButton > button::before'
        f' {{ content: "{chr(65 + index)}"; }}'
        for question in content.QUESTIONS
        for index in range(len(question["options"]))
    )


def _options_last_css() -> str:
    """Sin margen inferior en la última opción de cada pregunta."""
    selectors = ",\n".join(
        f'.st-key-flora_opt_{question["id"]}_{len(question["options"]) - 1}'
        for question in content.QUESTIONS
    )
    return f"{selectors} {{ margin-bottom: 0; }}"


BASE_CSS = "\n".join(
    [
        TOKENS, KEYFRAMES, SHELL, BUTTON_BASE, BLOCKS, CARDS,
        STEP1, STEP2, OPTIONS, SUMMARY, _letters_css(), _options_last_css(),
    ]
)


def selected_option_css(question_id: int, index: int) -> str:
    """Estado `.selected` de una opción: borde y badge en primary."""
    key = f".st-key-flora_opt_{question_id}_{index} .stButton > button"
    return (
        f"{key} {{ border-color: var(--primary) !important; color: var(--primary-dark) !important;"
        f" box-shadow: 0 0 0 2px rgba(124,58,237,0.15) !important; }}"
        f"{key}::before {{ background: var(--primary) !important; color: #fff !important; }}"
    )


def filled_field_css(field: str) -> str:
    """Campo de fecha/hora ya elegido."""
    key = f".st-key-flora_field_{field} .stButton > button"
    return (
        f"{key} {{ background: linear-gradient(135deg, var(--primary-light), #fff) !important;"
        f" border-color: var(--primary) !important; color: var(--primary-dark) !important;"
        f" box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important; }}"
    )


def selected_day_css(day: int) -> str:
    key = f".st-key-flora_day_{day} .stButton > button"
    return (
        f"{key} {{ background: var(--primary) !important; color: #fff !important;"
        f" font-weight: 800 !important; }}"
    )


def selected_minute_css(minute: int) -> str:
    key = f".st-key-flora_min_{minute} .stButton > button"
    return (
        f"{key} {{ border-color: var(--accent) !important;"
        f" background: var(--accent-light) !important; color: var(--accent) !important; }}"
    )


def escaping_no_css(attempts: int, left: float, top: float) -> str:
    """Réplica de `escapeNo()`: el "No" se encoge y salta, el "Sí" crece.

    `left` es una fracción (0..1): el desplazamiento se resuelve con `calc()` sobre el
    ancho de la tarjeta, reservando 84px para el ancho del botón, así el "No" nunca se
    sale de pantalla (clave en mobile) y sigue esquivando en cualquier ancho.
    """
    if attempts <= 0:
        return ""
    size = max(14 - attempts, 8)
    pad_y = max(12 - attempts * 2, 4)
    pad_x = max(24 - attempts * 3, 8)
    yes_size = min(18 + attempts * 4, 42)
    # El original topea el padding vertical en 32px pero calcula el horizontal a partir
    # del valor sin topear (llega a 60px en el último intento): se replica tal cual.
    yes_pad = min(16 + attempts * 4, 32)
    yes_pad_x = min(16 + attempts * 4 + 24, 64)
    return (
        f".st-key-flora_no {{ position: absolute !important;"
        f" left: calc((100% - 84px) * {left:.3f}) !important;"
        f" top: {top:.0f}px !important; z-index: 3; }}"
        f".st-key-flora_no .stButton > button {{ font-size: {size}px !important;"
        f" padding: {pad_y}px {pad_x}px !important; }}"
        f".st-key-flora_si .stButton > button {{ font-size: {yes_size}px !important;"
        f" padding: {yes_pad}px {yes_pad_x}px !important; }}"
    )


def inject(extra: str = "") -> None:
    st.markdown(f"<style>{BASE_CSS}\n{extra}</style>", unsafe_allow_html=True)
