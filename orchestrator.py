import subprocess
from pathlib import Path
from config import settings

RAW_DIR = Path("/app/volume/sast/raw")
FORMATTED_DIR = Path("/app/volume/sast/formatted")
AI_DIR = Path("/app/volume/sast/ai_analysis")

sastToRun = [s.strip().lower() for s in settings.SAST_TO_RUN.split(",")]

settings.validate()

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
    #Comando a ser executado: python Ai_sast_analysis/ai_analysis.py -l results/formatted_bandit.json  -o results/ai_results_bandit_chatGPT.json -ai "chat_gpt"
    #Passar somente a IA. O -l é pegado do diretório formatted e o -o vai para aquele caminho específico
    print("bang")


def main():

    run_sast(settings.BASE_DIRECTORY)
    run_formatting_scripts()

    print("[FINAL] Fluxo completo executado com sucesso !!!")

if __name__ == "__main__":
    main()