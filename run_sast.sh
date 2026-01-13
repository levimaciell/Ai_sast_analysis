#!/bin/sh

bandit -r "Ai_sast_analysis/vulnerable_files/files" -f json -o results/bandit.json
semgrep scan "Ai_sast_analysis/vulnerable_files/files" --json --json-output=results/semgrep.json