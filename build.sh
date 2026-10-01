#!/usr/bin/env bash
# Build para Cloudflare Pages (o cualquier hosting estático).
# Usa "flet publish": genera una web estática que corre Python en el navegador
# (Pyodide). NO necesita instalar Flutter, por eso es rápido y no pregunta nada.
set -euo pipefail

pip install "flet==1.0.0" "flet-cli==1.0.0" "flet-web==1.0.0"

flet publish main.py \
  --assets assets \
  --distpath dist \
  --app-name "Flet Widgets Playground" \
  --app-short-name "Flet Playground" \
  --app-description "Explora los widgets de Flet 1.0 en vivo"

echo "Listo: sitio estático en ./dist"
