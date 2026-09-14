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
    """Render a GitHub-compatible profile card without scripts or foreignObject."""
    name = escape(PROFILE["name"])
    role = escape(PROFILE["role"])
    location = escape(PROFILE["location"])
    avatar_markup = (
        f'<image href="{avatar}" x="857" y="89" width="210" height="210" '
        'clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>'
        if avatar
        else (
            '<circle cx="962" cy="194" r="105" fill="url(#avatar-fallback)"/>'
            '<text x="962" y="211" text-anchor="middle" fill="#ffffff" '
            'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            'font-size="62" font-weight="700">NTD</text>'
        )
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" role="img" aria-labelledby="title description">
  <title id="title">{name} animated profile card</title>
  <desc id="description">{role} based in {location}.</desc>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07152f"/><stop offset="0.47" stop-color="#35246d"/><stop offset="1" stop-color="#9b255f"/></linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.23"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.07"/></linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#57f5ff"/><stop offset="0.5" stop-color="#b48cff"/><stop offset="1" stop-color="#ff91d4"/></linearGradient>
    <radialGradient id="cyan" cx="0.16" cy="0.15" r="0.8"><stop offset="0" stop-color="#2de2e6" stop-opacity="0.78"/><stop offset="1" stop-color="#2de2e6" stop-opacity="0"/></radialGradient>
    <radialGradient id="pink" cx="0.85" cy="0.8" r="0.78"><stop offset="0" stop-color="#ff76ce" stop-opacity="0.72"/><stop offset="1" stop-color="#ff76ce" stop-opacity="0"/></radialGradient>
    <linearGradient id="avatar-fallback" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2de2e6"/><stop offset="1" stop-color="#a855f7"/></linearGradient>
    <clipPath id="avatar-clip"><circle cx="962" cy="194" r="105"/></clipPath>
    <filter id="blur"><feGaussianBlur stdDeviation="38"/></filter>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="16" stdDeviation="15" flood-color="#020617" flood-opacity="0.5"/></filter>
    <style>
      @keyframes drift-a {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(45px,18px); }} }}
      @keyframes drift-b {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(-38px,-20px); }} }}
      @keyframes pulse {{ 0%,100% {{ opacity:.32; transform:scaleY(.36); }} 50% {{ opacity:1; transform:scaleY(1); }} }}
      .orb-a {{ animation:drift-a 12s ease-in-out infinite; }} .orb-b {{ animation:drift-b 15s ease-in-out infinite; }}
      .bar {{ transform-box:fill-box; transform-origin:center bottom; animation:pulse 1.4s ease-in-out infinite; }}
      .bar:nth-child(2n) {{ animation-delay:-.35s; }} .bar:nth-child(3n) {{ animation-delay:-.7s; }} .bar:nth-child(5n) {{ animation-delay:-1.05s; }}
    </style>
  </defs>
  <rect width="1200" height="420" rx="28" fill="url(#background)"/>
  <circle class="orb-a" cx="156" cy="72" r="215" fill="url(#cyan)" filter="url(#blur)"/>
  <circle class="orb-b" cx="1075" cy="345" r="250" fill="url(#pink)" filter="url(#blur)"/>
  <g filter="url(#shadow)">
    <rect x="64" y="52" width="1072" height="316" rx="24" fill="url(#glass)" stroke="#ffffff" stroke-opacity=".35"/>
    <rect x="65" y="53" width="1070" height="73" rx="24" fill="#ffffff" fill-opacity=".06"/>
    <circle cx="103" cy="89" r="7" fill="#ff8cab"/><circle cx="128" cy="89" r="7" fill="#ffd36d"/><circle cx="153" cy="89" r="7" fill="#64e6a5"/>
    <text x="1094" y="95" text-anchor="end" fill="#d7f9ff" fill-opacity=".84" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="15" letter-spacing="2">PROFILE / LIVE</text>
    <rect x="108" y="160" width="12" height="130" rx="6" fill="url(#accent)"/>
    <text x="148" y="184" fill="#ccfbff" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="16" font-weight="700" letter-spacing="3">HELLO, WORLD</text>
    <text x="146" y="242" fill="#ffffff" font-family="system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="51" font-weight="700">{name}</text>
    <text x="148" y="281" fill="#ebddff" font-family="system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="24">{role}</text>
    <text x="148" y="323" fill="#d7f9ff" font-family="system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="18">{location}  ·  TypeScript  ·  React  ·  Next.js  ·  NestJS</text>
    <circle cx="962" cy="194" r="112" fill="none" stroke="url(#accent)" stroke-width="4"/>
    {avatar_markup}
    <g transform="translate(876 321)">''' + "".join(
        f'<rect class="bar" x="{index * 17}" y="{34 - height}" width="9" height="{height}" rx="4" fill="url(#accent)"/>'
        for index, height in enumerate((18, 31, 12, 35, 24, 39, 16, 29, 21, 37, 14, 30))
    ) + '''</g>
  </g>
</svg>'''


@app.get("/api/profile-card")
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
