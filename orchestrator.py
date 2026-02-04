import subprocess
from pathlib import Path
from config import settings
import os

RAW_DIR = Path("/app/volume/sast/raw")
FORMATTED_DIR = Path("/app/volume/sast/formatted")
AI_DIR = Path("/app/volume/sast/ai_analysis")

sastToRun = [s.strip().lower() for s in settings.SAST_TO_RUN.split(",")]
aiToRun = [a.strip().lower() for a in settings.AI_TO_RUN.split(",")]

settings.validate()

def validate_sast(sast:str):
    sastList = set(sastToRun)
    if sast not in sastList:
        raise RuntimeError(f"Unknown sast tool: {sast}")

def validate_ai(ai:str):
    aiList = set(aiToRun)
    if ai not in aiList:
        raise RuntimeError(f"Unknown Ai tool: {ai}")

#No caso de adicionar N ferramentas, considerar criar callers para SAST
def run_sast(target: str):

    commands = {
        'bandit': ["bandit", "-r", target, "-f", "json", "-o", str(RAW_DIR / "bandit.json")],
        'semgrep': ["semgrep", "scan", target, "--json", f"--json-output={RAW_DIR / 'semgrep.json'}"]
    }

    unknown = set(sastToRun) - commands.keys()
    if unknown:
        raise RuntimeError(f"Unknown SAST tools: {', '.join(unknown)}")

    for sast in sastToRun:
        print(f"[SAST] Executando ferramenta:  {sast}")
        result = subprocess.run(commands[sast], capture_output=True, text=True)

        if result.returncode not in (0, 1):
            raise RuntimeError(f"{sast} failed (exit code: {result.returncode}):\n{result.stderr}")

def run_formatting_scripts():

    commands = {
        'bandit': ["python", "bandit_parser.py", "-i", str(RAW_DIR / 'bandit.json'), "-o", str(FORMATTED_DIR / 'formatted_bandit.json')],
        'semgrep': ["python", "semgrep_parser.py", "-i", str(RAW_DIR / 'semgrep.json'), "-o", str(FORMATTED_DIR / 'formatted_semgrep.json')]
    }

    unknown = set(sastToRun) - commands.keys()
    if unknown:
        raise RuntimeError(f"Unknown SAST tools: {', '.join(unknown)}")
    
    for sast in sastToRun:
        print(f"[FORMATTING] Executandos scripts de padronização:  {sast}")
        result = subprocess.run(commands[sast], capture_output=True, text=True)

        if result.returncode not in (0, 1):
            raise RuntimeError(f"{sast} failed (exit code: {result.returncode}):\n{result.stderr}")
        

def run_ai_analysis(ai:str, sast:str):
    validate_ai(ai)
    validate_sast(sast)
    
    pathFormatted = FORMATTED_DIR / f'formatted_{sast}.json'
    pathSave = AI_DIR / sast / ai / f'ai_analysis_{sast}-{ai}.json'
    pathSave.parent.mkdir(parents=True, exist_ok=True)

    print(f'[{sast.upper()}-{ai.upper()}] ANALISANDO {sast} com {ai}')

    subprocess.run(["python", "ai_analysis.py", "-l", str(pathFormatted), "-o", str(pathSave), "-ai", ai], check=True)



# def main():
#     print('[STEP 1] Executando ferramentas de SAST')
#     run_sast(settings.BASE_DIRECTORY)

#     print('[STEP 2] Executando Scripts de formatação dos arquivos')
#     run_formatting_scripts()

#     print('[STEP 3] Executando análises de IA')
#     for ai in aiToRun:
#         for sast in sastToRun:
#             run_ai_analysis(ai, sast)

from concurrent.futures import ThreadPoolExecutor, as_completed

def main():
    print('[STEP 1] Executando ferramentas de SAST')
    run_sast(settings.BASE_DIRECTORY)

    print('[STEP 2] Executando Scripts de formatação dos arquivos')
    run_formatting_scripts()

    print('[STEP 3] Executando análises de IA')

    # tasks = []

    # with ThreadPoolExecutor(max_workers=len(aiToRun)) as executor:
    #     for ai in aiToRun:
    #         for sast in sastToRun:
    #             tasks.append(
    #                 executor.submit(run_ai_analysis, ai, sast)
    #             )

    # for future in as_completed(tasks):
    #     future.result()

    MAX_WORKERS = min(3, len(aiToRun))

    for sast in sastToRun:
        print(f"[{sast.upper()}] START")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(run_ai_analysis, ai, sast)
                for ai in aiToRun
            ]

            for future in as_completed(futures):
                future.result()
        
        print(f"[{sast.upper()}] END")

    print('Execução realizada com sucesso')

if __name__ == "__main__":
    main()