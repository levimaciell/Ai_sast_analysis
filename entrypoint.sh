#!/bin/sh
set -e

mkdir -p \
  /app/volume/sast/raw \
  /app/volume/sast/formatted \
  /app/volume/sast/ai_analysis

#Activating Bandit venv
. /app/bandit-env/bin/activate

exec python /app/orchestrator.py