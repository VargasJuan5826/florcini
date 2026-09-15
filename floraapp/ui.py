"""Bloques HTML para el plancito con Flora (modo gamer).

Deliberadamente sólo se usan `div`, `span`, `img` y `br`: Streamlit aplica sus propios
estilos a `h1`/`p`/`small` dentro del markdown, y usar elementos neutros evita esa pelea
de especificidad.
"""

from __future__ import annotations

from datetime import date

import streamlit as st

from . import assets, content


def html(markup: str) -> str:
    """Compacta el markup para que Streamlit no lo interprete como bloque markdown."""
    return "".join(line.strip() for line in markup.strip().splitlines())


def header() -> str:
    curr_exp = st.session_state.get("current_exp", content.BASE_EXP)
    prev_exp = st.session_state.get("prev_exp", content.BASE_EXP)
    earned = st.session_state.get("earned_exp", 0)
    step = st.session_state.get("step", 1)

    is_animated = earned > 0 and step >= 6
    fill_class = "rank-bar-fill animated-fill" if is_animated else "rank-bar-fill"

    bonus_badge = ""
    if is_animated:
        bonus_badge = f"""
        <div class="exp-levelup-badge">
          ✨ ¡+{earned} XP GANADOS! (Progreso subió a {curr_exp} / 100 XP) 🎮
        </div>
        """

    return html(
        f"""
        <div class="flora flora-header">
          <div class="flora-title">{content.TITLE}</div>
          <div class="flora-sub">{content.SUBTITLE}</div>
          <div class="gamer-rank-card">
            <div class="rank-season-tag">🎮 {content.RANK_SEASON}</div>
            <div class="rank-card-body">
              <div class="rank-badge-wrap">
                <img src="{assets.url(content.RANK_ICON)}" alt="{content.RANK_NAME}">
              </div>
              <div class="rank-details">
                <div class="rank-header-line">
                  <span class="rank-title-label">{content.RANK_TITLE}</span>
                  <span class="rank-name-value">{content.RANK_NAME}</span>
                </div>
                <div class="rank-bar-bg">
                  <div class="{fill_class}" style="--prev-w: {prev_exp}%; --curr-w: {curr_exp}%; width: {curr_exp}%;"></div>
                </div>
                <div class="rank-footer-line">
                  <span class="rank-hint-label">💡 {content.RANK_HINT}</span>
                  <span class="rank-percent-label">{curr_exp} / 100 XP</span>
                </div>
              </div>
            </div>
          </div>
          {bonus_badge}
        </div>
        """
    )


def plea_card() -> str:
    return html(
        f"""
        <div class="flora flora-step">
          <div class="plea-card">
            <img src="{assets.url(content.CAT_HEADER_IMG)}" alt="Fin de semana">
            <div class="plea-text">
              ¿Otro loquísimo fin de semana o sale plancito? 🎮
              <span class="plea-note">/* presiona iniciar para ver la misión */</span>
            </div>
          </div>
        </div>
        """
    )


def step1_intro() -> str:
    return html(
        f"""
        <div class="flora">
          <div class="step1-imgs">
            <img src="{assets.url('fin-de-semana.jfif')}" alt="Fin de semana">
          </div>
          <div class="step1-q">¿Sale plancito? 👀🎮</div>
        </div>
        """
    )


def no_message(attempts: int) -> str:
    text = (
        '// el botón "No" fue deshabilitado por el servidor 😼'
        if attempts >= 5
        else "// error: opción denegada en este lobby 😼"
    )
    return html(f'<div class="flora"><div class="flora-no-msg">{text}</div></div>')


def card_foot() -> str:
    return html('<div class="flora"><div class="flora-card-foot"></div></div>')


def step2_intro(chosen_plan: str | None = None) -> str:
    img_name = content.PLAN_IMAGES.get(chosen_plan, "fin-de-semana.jfif")
    is_resident_evil = chosen_plan and "resident evil" in chosen_plan.lower()
    tip_html = (
        '<div class="re-tip">// 🎬 disponible en IMAX entre el 17 y 20 de septiembre</div>'
        if is_resident_evil
        else ""
    )
    return html(
        f"""
        <div class="flora">
          <div class="flora-qhead-fixed">
            <img src="{assets.url(img_name)}" alt="Misión" class="fixed-option-img">
          </div>
          <span class="q-tag q-tag-agenda">// módulo: agenda.sync</span>
          <div class="step2-q">¿Cuándo te queda bien? 📅</div>
          {tip_html}
        </div>
        """
    )


def picker_label(text: str) -> str:
    return html(f'<div class="flora"><div class="picker-label">{text}</div></div>')


def month_label(value: date) -> str:
    name = content.MONTH_NAMES[value.month - 1]
    return html(f'<div class="flora"><div class="flora-cal-month">{name} de {value.year}</div></div>')


def weekdays() -> str:
    cells = "".join(f"<div>{day}</div>" for day in content.DAY_NAMES)
    return html(f'<div class="flora"><div class="flora-cal-week">{cells}</div></div>')


def clock_face(hour: int, minute: int) -> str:
    return html(
        f"""
        <div class="flora">
          <div class="flora-clock-face">
            <span class="hh">{hour:02d}</span>
            <span class="sep">:</span>
            <span class="mm">{minute:02d}</span>
          </div>
        </div>
        """
    )


def empty_day() -> str:
    return html('<div class="flora"><div class="flora-day-empty"></div></div>')


def progress(index: int) -> str:
    total = len(content.QUESTIONS)
    percent = round((index + 1) / total * 100)
    return html(
        f"""
        <div class="flora">
          <div class="flora-progress-label">misión {index + 1} / {total}</div>
          <div class="flora-progress-wrap">
            <div class="flora-progress-fill" style="width: {percent}%"></div>
          </div>
        </div>
        """
    )


def question_card(question: dict, chosen_option: str | None = None) -> str:
    image = content.PLAN_IMAGES.get(chosen_option, content.QUESTION_HEADER_IMAGES.get(question["id"], content.CAT_HEADER_IMG))
    return html(
        f"""
        <div class="flora flora-step">
          <div class="flora-qhead-fixed">
            <img src="{assets.url(image)}" alt="Misión" class="fixed-option-img">
          </div>
          <div class="q-card">
            <span class="q-tag">{question['tag']}</span>
            <div class="q-text">{question['text']}</div>
          </div>
        </div>
        """
    )


def error(text: str) -> str:
    return html(f'<div class="flora"><div class="err-msg">{text}</div></div>')


def summary(answers: dict) -> str:
    rows = []
    for position, (icon, label, key) in enumerate(content.SUMMARY_ROWS):
        value = answers.get(key) or "—"
        alt = " alt" if position % 2 == 1 else ""
        rows.append(
            f'<div class="summary-row{alt}"><span class="s-icon">{icon}</span>'
            f'<span class="s-label">{label}</span>'
            f'<span class="s-value">{value}</span></div>'
        )
    chosen_plan = answers.get(2)
    summary_img = content.PLAN_IMAGES.get(chosen_plan, content.CAT_HEADER_IMG)
    return html(
        f"""
        <div class="flora flora-step">
          <div class="summary-header">
            <div class="flora-qhead-fixed" style="margin: 0 auto 12px;">
              <img src="{assets.url(summary_img)}" alt="Gato resumen" class="fixed-option-img">
            </div>
            <div class="summary-title">Resumen del Plancito</div>
            <div class="summary-note">// coordinación completada · estado: listo 🎮</div>
          </div>
          <div class="summary-table">{''.join(rows)}</div>
          <div class="final-card">
            <div class="q-text">¿Confirmamos el plancito? 😎</div>
            <div class="final-note">// advertencia: arrepentirse resta puntos de rango 😼</div>
          </div>
        </div>
        """
    )


def finale() -> str:
    return html(
        f"""
        <div class="flora">
          <div class="finale">
            <div class="finale-imgs">
              <img src="{assets.url('michi-tomando.jfif')}" alt="michi tomando">
              <img src="{assets.url('fin-de-semana.jfif')}" alt="fin de semana">
              <img src="{assets.url('gato-ada-wong.jpg')}" alt="gato ada wong">
            </div>
            <div class="finale-title">¡Misión coordinada! 🎮</div>
            <div class="finale-note">// status: PLAN CONFIRMADO<br>// Descargá el PDF y mandámelo x chat para agendar 😎</div>
          </div>
        </div>
        """
    )


def cat_rain(cats: list[dict]) -> str:
    images = "".join(
        f'<img class="float-cat" src="{assets.url(content.FLOAT_CAT_SRCS[cat["pick"]])}"'
        f' style="left: {cat["left"]:.1f}%; animation-duration: {cat["duration"]:.2f}s;'
        f' animation-delay: {cat["delay"]:.2f}s" alt="">'
        for cat in cats
    )
    return html(f'<div class="flora flora-rain">{images}</div>')

