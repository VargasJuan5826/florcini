"""Textos, preguntas y assets para el plancito con Flora."""

RANK_TITLE = "Rango Actual :"
RANK_NAME = "Conocido 1"
BASE_EXP = 35
RANK_ICON = "bronce-1.jpg"

QUESTIONS = [
    {
        "id": 2,
        "tag": "// misión: seleccionar_plan.cfg",
        "text": "🎮 ¿Qué plan sale para coordinar?",
        "options": [
            "🚶 Salir a caminar  +20 pts",
            "🍻 Salir a tomar algo  +30 pts",
            "🎬 Ir al IMAX a ver Resident Evil (entre el 17 y 20 de septiembre)  +50 pts",
        ],
    },
]

# Puntos de EXP por cada opción
PLAN_POINTS = {
    "🚶 Salir a caminar  +20 pts": 20,
    "🍻 Salir a tomar algo  +30 pts": 30,
    "🎬 Ir al IMAX a ver Resident Evil (entre el 17 y 20 de septiembre)  +50 pts": 50,
}

# Mapa de imagen según opción elegida (todas al mismo tamaño)
PLAN_IMAGES = {
    "🚶 Salir a caminar  +20 pts": "cj-caminando.jpg",
    "🍻 Salir a tomar algo  +30 pts": "michi-tomando.jfif",
    "🎬 Ir al IMAX a ver Resident Evil (entre el 17 y 20 de septiembre)  +50 pts": "gato-ada-wong.jpg",
}

QUESTION_HEADER_IMAGES = {
    2: "fin-de-semana.jfif",
}

CAT_HEADER_IMG = "fin-de-semana.jfif"
CAT_IMAGES_STEP1 = ["fin-de-semana.jfif"]
CAT_IMAGES_STEP2 = ["fin-de-semana.jfif", "michi-tomando.jfif"]
FLOAT_CAT_SRCS = ["fin-de-semana.jfif", "michi-tomando.jfif", "gato-ada-wong.jpg", "cj-caminando.jpg"]

# Filas del resumen: (icono, etiqueta, clave de respuesta)
SUMMARY_ROWS = [
    ("🎮", "rango://", "rank"),
    ("📍", "plan://", 2),
    ("📅", "horario://", 6),
]

# Íconos para el botón "Sí" (gamer/chill, sin corazones)
SI_ICONS = ["😎", "🎮", "🕹️", "🔥", "👾", "😂"]

TITLE = "Flora"
SUBTITLE = "// matchmaking: casual_party.lobby"

# Música de fondo: ID del video de YouTube solicitado (https://youtu.be/7vG4knGrP9w?t=742)
MUSIC_VIDEO_ID = "7vG4knGrP9w"
MUSIC_START_SECONDS = 742

DAY_NAMES = ["D", "L", "M", "X", "J", "V", "S"]
MONTH_NAMES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]
