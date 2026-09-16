"""Música de fondo con un embed (oculto) de YouTube y una barra de reproductor propia.

Dos restricciones que definen el diseño:

* **Autoplay con sonido:** los navegadores lo bloquean hasta que hay un gesto del usuario.
  Por eso la música arranca en el primer click (el botón "INICIAR"): ese gesto habilita el
  audio, y como es lo primero que se toca, se siente automático.
* **Persistencia entre reruns:** Streamlit recrea los iframes de `components.html` en cada
  rerun, así que un player montado ahí se reiniciaría al cambiar de paso. Para evitarlo, el
  iframe del componente sólo hace de *bootstrap*: inyecta —una única vez, con guarda— un
  `<script>` en el documento padre. Ese script corre en el contexto del padre (fuera del
  árbol de React de Streamlit, colgado de `document.body`), así el player, su barra de
  reproductor y el estado sobreviven a los reruns y a los cambios de paso.

El video de YouTube va oculto; lo que se ve es una barra propia (play/pausa, tiempo, una
barra para scrubbear/adelantar y mute) construida sobre la IFrame API de YouTube.
"""

from __future__ import annotations

import json

import streamlit.components.v1 as components

# Corre en el documento PADRE (lo inyecta el bootstrap). `window` es la ventana principal.
_PARENT_SCRIPT = r"""
(function () {
  var PLAYLIST = __PLAYLIST_JSON__;
  if (!PLAYLIST || !PLAYLIST.length) {
    PLAYLIST = [{ id: "odouCACH9-w", start: 1714, title: "Eurodance Nostalgia" }];
  }

  // Cada vez que se abre la app, se elige un tema al azar
  var currentIndex = Math.floor(Math.random() * PLAYLIST.length);
  var currentTrack = PLAYLIST[currentIndex];

  var state = {
    ready: false,
    started: false,
    muted: false,
    want: false,
    seeking: false,
    player: null,
    currentIndex: currentIndex,
    playlist: PLAYLIST
  };
  window.__floraMusic = state;

  // Estilos de la barra
  var css = document.createElement('style');
  css.textContent =
    '#flora-music-bar{position:fixed;top:0;left:0;right:0;width:100%;z-index:9998;' +
    'background:#ffffff;border-bottom:1px solid #ece9fb;box-shadow:0 2px 10px rgba(124,58,237,0.10);' +
    "font-family:'Nunito',sans-serif;box-sizing:border-box;}" +
    '#flora-music-inner{max-width:560px;margin:0 auto;display:flex;align-items:center;gap:10px;' +
    'padding:8px 14px;box-sizing:border-box;}' +
    '#flora-music-bar button{border:none;background:none;cursor:pointer;padding:0;color:#5b21b6;' +
    'display:flex;align-items:center;justify-content:center;line-height:1;' +
    'transition:transform 0.15s ease, color 0.15s ease;}' +
    '#flora-music-play{width:30px;height:30px;border-radius:50%;flex:0 0 auto;' +
    'background:linear-gradient(135deg,#7c3aed,#ec4899)!important;color:#fff!important;font-size:14px;}' +
    '#flora-music-prev,#flora-music-next{width:24px;height:24px;flex:0 0 auto;color:#7c3aed;font-size:13px;opacity:0.85;}' +
    '#flora-music-prev:hover,#flora-music-next:hover{opacity:1;transform:scale(1.15);color:#5b21b6;}' +
    '#flora-music-mute{font-size:16px;flex:0 0 auto;}' +
    '#flora-music-bar .flora-t{font-size:10px;color:#6b7280;font-variant-numeric:tabular-nums;flex:0 0 auto;min-width:28px;text-align:center;}' +
    '#flora-music-seek{-webkit-appearance:none;appearance:none;flex:1 1 auto;height:4px;border-radius:2px;' +
    'background:#e9e5f7;outline:none;cursor:pointer;}' +
    '#flora-music-seek::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:13px;height:13px;' +
    'border-radius:50%;background:#7c3aed;cursor:pointer;box-shadow:0 1px 3px rgba(124,58,237,0.5);}' +
    '#flora-music-seek::-moz-range-thumb{width:13px;height:13px;border-radius:50%;background:#7c3aed;border:none;cursor:pointer;}' +
    '[data-testid="stAppViewContainer"] [data-testid="stMainBlockContainer"]{padding-top:60px!important;}';
  document.head.appendChild(css);

  // Host para el player de YouTube
  var host = document.createElement('div');
  host.id = 'flora-yt-host';
  host.style.cssText = 'position:fixed;bottom:0;right:0;width:200px;height:200px;opacity:0.001;pointer-events:none;z-index:-9999;';
  var slot = document.createElement('div');
  slot.id = 'flora-yt-player';
  host.appendChild(slot);
  document.body.appendChild(host);

  // Barra de reproductor con Anterior y Siguiente
  var bar = document.createElement('div');
  bar.id = 'flora-music-bar';
  bar.innerHTML =
    '<div id="flora-music-inner">' +
    '<button id="flora-music-prev" type="button" aria-label="Anterior" title="Tema anterior">⏮</button>' +
    '<button id="flora-music-play" type="button" aria-label="Play/Pausa">▶</button>' +
    '<button id="flora-music-next" type="button" aria-label="Siguiente" title="Siguiente tema">⏭</button>' +
    '<span class="flora-t" id="flora-music-cur">0:00</span>' +
    '<input id="flora-music-seek" type="range" min="0" max="100" value="0" step="0.1" aria-label="Adelantar">' +
    '<span class="flora-t" id="flora-music-dur">0:00</span>' +
    '<button id="flora-music-mute" type="button" aria-label="Silenciar">🔊</button>' +
    '</div>';
  document.body.appendChild(bar);

  var playBtn = document.getElementById('flora-music-play');
  var prevBtn = document.getElementById('flora-music-prev');
  var nextBtn = document.getElementById('flora-music-next');
  var muteBtn = document.getElementById('flora-music-mute');
  var seek = document.getElementById('flora-music-seek');
  var curEl = document.getElementById('flora-music-cur');
  var durEl = document.getElementById('flora-music-dur');

  if (PLAYLIST.length <= 1) {
    if (prevBtn) prevBtn.style.display = 'none';
    if (nextBtn) nextBtn.style.display = 'none';
  }

  function fmt(s) {
    s = Math.max(0, Math.floor(s || 0));
    var m = Math.floor(s / 60);
    var r = s % 60;
    return m + ':' + (r < 10 ? '0' : '') + r;
  }
  function isPlaying() {
    try { return state.player && state.player.getPlayerState() === 1; } catch (e) { return false; }
  }

  function start() {
    if (!state.player || !state.ready) { state.want = true; return; }
    try {
      state.player.playVideo();
      state.player.unMute();
      state.player.setVolume(30);
      state.started = true;
      state.muted = false;
      muteBtn.textContent = '🔊';
    } catch (e) {}
  }
  function toggleMute() {
    if (!state.player) return;
    if (state.muted) { try { state.player.unMute(); } catch (e) {} state.muted = false; }
    else { try { state.player.mute(); } catch (e) {} state.muted = true; }
    muteBtn.textContent = state.muted ? '🔇' : '🔊';
  }

  function loadTrack(idx) {
    if (idx < 0) idx = PLAYLIST.length - 1;
    if (idx >= PLAYLIST.length) idx = 0;
    currentIndex = idx;
    currentTrack = PLAYLIST[currentIndex];
    state.currentIndex = currentIndex;
    seek.value = 0;
    curEl.textContent = '0:00';
    if (state.player && typeof state.player.loadVideoById === 'function') {
      try {
        state.player.loadVideoById({
          videoId: currentTrack.id,
          startSeconds: currentTrack.start || 0
        });
        state.player.playVideo();
        state.player.unMute();
        state.player.setVolume(30);
      } catch (e) {}
    }
  }

  function nextTrack() {
    loadTrack(currentIndex + 1);
  }

  function prevTrack() {
    loadTrack(currentIndex - 1);
  }

  playBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    if (!state.player) return;
    try {
      if (isPlaying()) {
        state.player.pauseVideo();
      } else {
        start();
        state.player.playVideo();
      }
    } catch (e2) {}
  });
  prevBtn.addEventListener('click', function (e) { e.stopPropagation(); prevTrack(); });
  nextBtn.addEventListener('click', function (e) { e.stopPropagation(); nextTrack(); });
  muteBtn.addEventListener('click', function (e) { e.stopPropagation(); toggleMute(); });

  // Scrubbear / adelantar
  seek.addEventListener('input', function () { state.seeking = true; curEl.textContent = fmt(seek.value); });
  var commitSeek = function () {
    var v = parseFloat(seek.value);
    try { state.player.seekTo(v, true); } catch (e) {}
    curEl.textContent = fmt(v);
    setTimeout(function () { state.seeking = false; }, 800);
  };
  seek.addEventListener('change', commitSeek);
  seek.addEventListener('pointerup', commitSeek);
  seek.addEventListener('click', function (e) { e.stopPropagation(); });

  // Refresco de la barra
  setInterval(function () {
    if (!state.player || !state.ready) return;
    try {
      var d = state.player.getDuration() || 0;
      var t = state.player.getCurrentTime();
      if (d && parseFloat(seek.max) !== d) { seek.max = d; durEl.textContent = fmt(d); }
      if (!state.seeking && typeof t === 'number' && isFinite(t) && t >= 0 && (!d || t <= d + 1)) {
        seek.value = t; curEl.textContent = fmt(t);
      }
      playBtn.textContent = isPlaying() ? '⏸' : '▶';
    } catch (e) {}
  }, 400);

  // Desmutear con cualquier interacción si el navegador requirió gesto previo
  var unlockSound = function () {
    if (!state.player) return;
    try {
      state.player.unMute();
      state.player.setVolume(30);
      state.player.playVideo();
      state.muted = false;
      muteBtn.textContent = '🔊';
    } catch (e) {}
  };
  ['click', 'touchstart', 'touchend', 'pointerdown', 'mousedown', 'keydown'].forEach(function (ev) {
    document.addEventListener(ev, unlockSound, { capture: true, passive: true });
    window.addEventListener(ev, unlockSound, { capture: true, passive: true });
  });

  // API de YouTube (en el documento padre).
  function makePlayer() {
    state.player = new window.YT.Player('flora-yt-player', {
      videoId: currentTrack.id,
      playerVars: {
        autoplay: 1,
        mute: 1,
        controls: 0,
        playsinline: 1,
        modestbranding: 1,
        rel: 0,
        fs: 0,
        disablekb: 1,
        start: currentTrack.start || 0,
        origin: window.location.origin
      },
      events: {
        onReady: function () {
          state.ready = true;
          if (currentTrack.start > 0) {
            try { state.player.seekTo(currentTrack.start, true); } catch (e) {}
          }
          // Reproducir inmediatamente
          try {
            state.player.playVideo();
          } catch (e) {}
          // Intentar desmutear de una
          try {
            state.player.unMute();
            state.player.setVolume(30);
            if (!state.player.isMuted()) {
              state.muted = false;
              muteBtn.textContent = '🔊';
            }
          } catch (e) {}
        },
        onStateChange: function (ev) {
          if (ev.data === window.YT.PlayerState.PLAYING) {
            state.started = true;
            playBtn.textContent = '⏸';
          } else if (ev.data === window.YT.PlayerState.PAUSED) {
            playBtn.textContent = '▶';
          } else if (ev.data === window.YT.PlayerState.ENDED) {
            if (PLAYLIST.length > 1) {
              nextTrack();
            } else {
              try {
                ev.target.seekTo(currentTrack.start || 0, true);
                ev.target.playVideo();
              } catch (e) {}
            }
          }
        }
      }
    });
  }
  if (window.YT && window.YT.Player) {
    makePlayer();
  } else {
    var prev = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = function () {
      if (typeof prev === 'function') { try { prev(); } catch (e) {} }
      makePlayer();
    };
    if (!document.getElementById('flora-yt-api')) {
      var tag = document.createElement('script');
      tag.id = 'flora-yt-api';
      tag.src = 'https://www.youtube.com/iframe_api';
      document.head.appendChild(tag);
    }
  }
})();
"""

_BOOTSTRAP = r"""
<script>
(function () {
  var pdoc, pwin;
  try { pdoc = window.parent.document; pwin = window.parent; } catch (e) { return; }
  if (!pdoc || !pdoc.body) return;

  var SCRIPT_VER = 6;
  if (pwin.__floraMusicInjected && pwin.__floraMusicVersion === SCRIPT_VER) {
    if (pwin.__floraMusic && pwin.__floraMusic.player && typeof pwin.__floraMusic.player.playVideo === 'function') {
      try {
        pwin.__floraMusic.player.playVideo();
        pwin.__floraMusic.player.unMute();
      } catch (e) {}
    }
    return;
  }

  // Limpiar elementos de versión previa
  var oldBar = pdoc.getElementById('flora-music-bar');
  if (oldBar) oldBar.remove();
  var oldHost = pdoc.getElementById('flora-yt-host');
  if (oldHost) oldHost.remove();

  pwin.__floraMusicInjected = true;
  pwin.__floraMusicVersion = SCRIPT_VER;
  var s = pdoc.createElement('script');
  s.textContent = __PARENT_SCRIPT__;
  pdoc.body.appendChild(s);
})();
</script>
"""


def background(playlist_or_id: list[dict] | str, start_seconds: int = 0) -> None:
    """Monta (una sola vez) la música de fondo en playlist con selección aleatoria al abrir."""
    if isinstance(playlist_or_id, str):
        playlist = [{"id": playlist_or_id, "start": start_seconds, "title": "Track 1"}]
    else:
        playlist = playlist_or_id

    playlist_json = json.dumps(playlist)
    parent = (
        _PARENT_SCRIPT
        .replace("__PLAYLIST_JSON__", playlist_json)
    )
    literal = json.dumps(parent).replace("</", "<\\/")
    bootstrap = (
        _BOOTSTRAP
        .replace("__PARENT_SCRIPT__", literal)
    )
    components.html(bootstrap, height=0)

