#!/bin/sh

bandit -r "Ai_sast_analysis/vulnerable_files/files" -f json -o results/bandit.json
semgrep scan "Ai_sast_analysis/vulnerable_files/files" --json --json-output=results/semgrep.json

python Ai_sast_analysis/bandit_parser.py -i results/bandit.json -o results/formatted_bandit.json
python Ai_sast_analysis/semgrep_parser.py -i results/semgrep.json -o results/formatted_semgrep.json