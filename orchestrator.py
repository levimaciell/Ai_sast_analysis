import subprocess
from pathlib import Path
from config import settings

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
        print(f"[FORMATTING SAST] Executandos scripts de padronização:  {sast}")
        result = subprocess.run(commands[sast], capture_output=True, text=True)

        if result.returncode not in (0, 1):
            raise RuntimeError(f"{sast} failed (exit code: {result.returncode}):\n{result.stderr}")
        

def run_ai_analysis(ai:str, sast:str):
    validate_ai(ai)
    validate_sast(sast)
    
    pathFormatted = FORMATTED_DIR / f'formatted_{sast}.json'
    pathSave = AI_DIR / sast / ai / f'ai_analysis_{sast}-{ai}.json'
    pathSave.parent.mkdir(parents=True, exist_ok=True)

    print(f'[AI_ANALYSIS] ANALISANDO {pathFormatted} com {ai}')

    subprocess.run(["python", "ai_analysis.py", "-l", str(pathFormatted), "-o", str(pathSave), "-ai", ai], check=True)

    print('[AI_ANALYSIS] Execução realizada com sucesso')


def main():

    run_sast(settings.BASE_DIRECTORY)
    run_formatting_scripts()

    for ai in aiToRun:
        for sast in sastToRun:
            run_ai_analysis(ai, sast)

    print("[FINAL] Fluxo completo executado com sucesso !!!")

if __name__ == "__main__":
    main()