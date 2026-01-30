#!/bin/sh

bandit -r "vulnerable_files/files" -f json -o volume/sast/raw/bandit.json
semgrep scan vulnerable_files/files --json --json-output=volume/sast/raw/semgrep.json

# python Ai_sast_analysis/bandit_parser.py -i results/bandit.json -o results/formatted_bandit.json
# python Ai_sast_analysis/semgrep_parser.py -i results/semgrep.json -o results/formatted_semgrep.json