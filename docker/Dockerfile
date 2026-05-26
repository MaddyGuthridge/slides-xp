# slides-xp
# Serve your slides from an isolated container
FROM python:3.14-trixie

LABEL org.opencontainers.image.source="https://github.com/MaddyGuthridge/slides-xp"
LABEL org.opencontainers.image.description="A home-made, ultra-janky, Windows XP-themed markdown slideshow viewer."
LABEL org.opencontainers.image.licenses=GPL-3.0-only

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY README.md ./

RUN uv sync --no-dev --no-install-project

COPY slides_xp ./slides_xp

RUN uv sync --no-dev

RUN useradd -ms /bin/bash granian

WORKDIR /home/granian
USER granian
RUN mkdir data

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 3000

ENTRYPOINT ["python", "-m", "slides_xp", "/app/slides"]
