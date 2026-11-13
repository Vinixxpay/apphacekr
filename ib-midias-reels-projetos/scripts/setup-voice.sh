#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-voice.txt
mkdir -p work/models
curl -fL --retry 2 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx' -o work/models/kokoro.onnx
curl -fL --retry 2 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin' -o work/models/voices.bin
.venv/bin/python scripts/voice.py
.venv/bin/python scripts/align.py

.venv/bin/python scripts/mouth.py
.venv/bin/python scripts/effects.py
