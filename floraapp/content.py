"""Textos, preguntas y assets para el plancito con Flora."""

RANK_SEASON = "Temporada 1"
RANK_TITLE = "Rango Actual :"
RANK_NAME = "Chico extraño I"
RANK_HINT = "Elegí una misión para ganar experiencia"
BASE_EXP = 35
RANK_ICON = "bronce-1.jpg"

QUESTIONS = [
    {
        "id": 2,
        "tag": "// misión: seleccionar_plan.cfg",
        "text": "🎮 ¿Qué plan sale para coordinar?",
        "options": [
            "🚶 Salir a caminar  +20 XP",
            "🍻 Salir a tomar algo  +30 XP",
            "🎬 Ir al IMAX a ver Resident Evil (entre el 17 y 20 de septiembre)  +50 XP",
        ],
    },
]

# Puntos de XP por cada opción
PLAN_POINTS = {
    "🚶 Salir a caminar  +20 XP": 20,
    "🍻 Salir a tomar algo  +30 XP": 30,
    "🎬 Ir al IMAX a ver Resident Evil (entre el 17 y 20 de septiembre)  +50 XP": 50,
}

# Mapa de imagen según opción elegida (todas al mismo tamaño)
PLAN_IMAGES = {
    "🚶 Salir a caminar  +20 XP": "cj-caminando.jpg",
    "🍻 Salir a tomar algo  +30 XP": "michi-tomando.jfif",
    "🎬 Ir al IMAX a ver Resident Evil (entre el 17 y 20 de septiembre)  +50 XP": "gato-ada-wong.jpg",
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

# Playlist de fondo: actualmente con 1 tema.
# Podés agregar más videos cuando quieras con su id y segundo de inicio.
PLAYLIST = [
    {
        "id": "odouCACH9-w",
        "start": 1714,
        "title": "Eurodance Nostalgia",
    },
]

MUSIC_VIDEO_ID = PLAYLIST[0]["id"]
MUSIC_START_SECONDS = PLAYLIST[0]["start"]

DAY_NAMES = ["D", "L", "M", "X", "J", "V", "S"]
MONTH_NAMES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]
