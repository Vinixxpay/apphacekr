#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_CACHE_DIR="${UV_CACHE_DIR:-$PWD/.cache/uv}"
model_dir="$PWD/.cache/piper"
mkdir -p "$model_dir"
for filename in pt_BR-faber-medium.onnx pt_BR-faber-medium.onnx.json; do
  if [ ! -s "$model_dir/$filename" ]; then
    curl -fL --retry 2 "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/$filename" -o "$model_dir/$filename"
  fi
done
(
  cd "$model_dir"
  printf '%s\n' \
    '858555e3a064209c57088fe6bd70c4c3dc54d03eaa00c45d5ecaf43a33f95aa7  pt_BR-faber-medium.onnx' \
    '7e694de195ae3fc36dd732c445eb04fb49b649854893cb5506b978f0d50a1d6f  pt_BR-faber-medium.onnx.json' | sha256sum -c -
)
if [ ! -x .venv/bin/python ]; then uv venv .venv; fi
uv pip install --python .venv/bin/python -r requirements-voice.txt
PIPER_MODEL="$model_dir/pt_BR-faber-medium.onnx" .venv/bin/python scripts/audio.py
