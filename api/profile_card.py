"""Animated, self-contained SVG profile card for GitHub README embeds."""

from __future__ import annotations

from base64 import b64encode
from html import escape
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Flask, Response

app = Flask(__name__)

AVATAR_URL = "https://avatars.githubusercontent.com/duong-vn"
MAX_AVATAR_BYTES = 2 * 1024 * 1024
PROFILE = {
    "name": "Nguyen Tuan Duong",
    "role": "Software Engineer Intern · Frontend / Full-stack",
    "location": "Hanoi, Vietnam",
}


def load_avatar() -> str | None:
    """Return the fixed GitHub avatar as a safe inline image data URI."""
    request = Request(AVATAR_URL, headers={"User-Agent": "duong-vn-profile-card/1.0"})
    try:
        with urlopen(request, timeout=3) as response:  # noqa: S310 - fixed HTTPS URL
            content_type = response.headers.get_content_type()
            length = response.headers.get("Content-Length")
            if content_type not in {"image/jpeg", "image/png", "image/webp"}:
                return None
            if length and int(length) > MAX_AVATAR_BYTES:
                return None
            data = response.read(MAX_AVATAR_BYTES + 1)
    except (HTTPError, URLError, TimeoutError, ValueError):
        return None

    if len(data) > MAX_AVATAR_BYTES:
        return None
    return f"data:{content_type};base64,{b64encode(data).decode('ascii')}"


def render_card(avatar: str | None) -> str:
    """Render a GitHub-compatible animated profile card without music metadata."""
    name = escape(PROFILE["name"])
    role = escape(PROFILE["role"])
    avatar_markup = (
        f'<image href="{avatar}" x="20" y="20" width="167" height="167" '
        'clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>'
        if avatar
        else (
            '<rect x="20" y="20" width="167" height="167" rx="12" fill="#0d3338"/>'
            '<text x="103.5" y="112" text-anchor="middle" dominant-baseline="middle" '
            'fill="#8ad9d5" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            'font-size="44" font-weight="700">NTD</text>'
        )
    )
    # ponytail: decorative 60-bar pattern — upgrade when live audio data is intentionally added.
    heights = (51, 69, 78, 63, 58, 52, 49, 46, 42, 62, 70, 48, 77, 42, 72, 57, 39, 54, 67, 76, 50, 44, 65, 73, 57, 68, 45, 61, 74, 48, 43, 52, 49, 71, 41, 58, 64, 55, 46, 51, 59, 65, 76, 72, 48, 55, 61, 70, 75, 64, 51, 46, 42, 39, 44, 48, 53, 61, 69, 66)
    bars = "".join(
        f'<rect class="bar" x="{215 + index * 11}" y="{187 - height}" width="8" '
        f'height="{height}" rx="3" fill="url(#equalizer)"/>'
        for index, height in enumerate(heights)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 207" role="img" aria-labelledby="title description">
  <title id="title">{name} profile card</title>
  <desc id="description">{role}.</desc>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#09272a"/>
      <stop offset="1" stop-color="#041517"/>
    </linearGradient>
    <linearGradient id="equalizer" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#19777a"/>
      <stop offset="1" stop-color="#82cbc9"/>
    </linearGradient>
    <clipPath id="avatar-clip"><rect x="20" y="20" width="167" height="167" rx="12"/></clipPath>
    <style>
      @keyframes equalize {{ 0%, 100% {{ opacity: .55; transform: scaleY(.42); }} 50% {{ opacity: 1; transform: scaleY(1); }} }}
      .bar {{ transform-box: fill-box; transform-origin: center bottom; animation: equalize 1.4s ease-in-out infinite; }}
      .bar:nth-child(2n) {{ animation-delay: -.3s; animation-duration: 1.15s; }}
      .bar:nth-child(3n) {{ animation-delay: -.7s; animation-duration: 1.55s; }}
      .bar:nth-child(5n) {{ animation-delay: -1.1s; animation-duration: .95s; }}
    </style>
  </defs>
  <rect width="900" height="207" rx="13" fill="url(#background)" stroke="#165257" stroke-width="1.5"/>
  {avatar_markup}
  <text x="550" y="51" text-anchor="middle" fill="#bde4e2" font-family="system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="30" font-weight="600">{name}</text>
  <text x="550" y="93" text-anchor="middle" fill="#56a8a8" font-family="system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="17">{role}</text>
  <g>{bars}</g>
</svg>'''


@app.get("/api/profile-card")
@app.get("/api/profile_card.py")
def profile_card() -> Response:
    """Serve the animated profile card as SVG."""
    response = Response(render_card(load_avatar()), mimetype="image/svg+xml")
    response.headers["Cache-Control"] = "public, max-age=1800, s-maxage=1800, stale-while-revalidate=86400"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.get("/health")
def health() -> Response:
    """Serve deployment health status."""
    return Response("OK", mimetype="text/plain")
