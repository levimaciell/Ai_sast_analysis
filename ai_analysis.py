import argparse
import json
import os
import time
from ai_callers import GeminiCaller, ChatGptCaller, DeepseekCaller, ClaudeCaller
from config import settings

MAX_TRIES = settings.MAX_RETRY_ATTEMPTS
RETRY_DELAY = settings.RETRY_DELAY_SECONDS
BASE_DIRECTORY = settings.BASE_DIRECTORY

def build_prompt(vul_code: str, labels2: list[str]) -> str:
    return (
        "Which of the following vulnerabilities from list of vulnerabilities exist "
        "in the python code which is delimited with triple backticks. also give the "
        "number of the line of the vulnerability in the code.\n\n"
        f"Python code:\n'''\n{vul_code}\n'''\n\n"
        "List of vulnerabilities:\n"
        + ", ".join(labels2) +
        "\n\nFormat your response as a list of JSON objects with \"label\" and \"line of Code\" "
        "as the keys for each element. Only answer with JSON."
    )

def getAiCaller(ai: str):
    callers = {
        "gemini": GeminiCaller,
        "chat_gpt": ChatGptCaller,
        "deepseek": DeepseekCaller,
        "claude": ClaudeCaller
    }

    try:        
        return callers[ai]()
    
    except KeyError:
        raise ValueError(
            f"IA inválida: {ai}. Use uma das seguintes: {', '.join(callers)}"
        )

def main():
    parser = argparse.ArgumentParser(description="Executa IA como assistente SAST em todos os arquivos python que existirem em um diretório")

    parser.add_argument("-l", required=True, help="Arquivo json contendo a análise feita pela ferramenta de sast")
    parser.add_argument("-o", required=True, help="Caminho do output gerado pela IA")
    parser.add_argument("-ai", required=True, help="Nome da IA a ser utilizada")

    args = parser.parse_args()

    Caller = getAiCaller(args.ai)

    with open(args.l, "r", encoding="utf-8") as f:
        listaSast = json.load(f)

    arquivosComLabel = {
        os.path.basename(item["filename"]) for item in listaSast
    }

    #Criando dicionário contendo os filenames e as labels
    labelsByFile = {}

    for item in listaSast:
        fname = os.path.basename(item["filename"])
        labelsByFile.setdefault(fname, []).extend(item["labels"])

    # Guarda os paths dos arquivos que contém algum tipo de vulnerabilidade
    filesToProcess = []
    for root, _, files in os.walk(BASE_DIRECTORY):
        for file in files:
            if file.endswith(".py") and os.path.basename(file) in arquivosComLabel :
                filesToProcess.append(os.path.join(root,file))

    results = []
    processed = 0


    for filePath in filesToProcess:
        processed += 1

        filename = os.path.basename(filePath)

        with open(filePath, "r", encoding="utf-8") as f:
            code = f.read()

        labels = []
        for item in labelsByFile.get(filename):
            labels.append(item['cwe'])

        prompt = build_prompt(code, labels)
        
        success = False
        last_error = None

        for attempt in range(1, MAX_TRIES, + 1):
            try:

                ai_result = Caller.requestAi(prompt)
                 
                success = True
                break
            
            except json.JSONDecodeError:
                last_error = "Invalid JSON"
                print("   ⚠️ JSON inválido retornado pela IA")

            except Exception as e:
                last_error = str(e)
                print(f"   ⚠️ Erro de requisição: {last_error}")
                print(e)

            if attempt < MAX_TRIES:
                time.sleep(RETRY_DELAY)
        
        if not success:
            raise RuntimeError(f"❌ Falha definitiva em {filePath}\n")
            
        else:
            results.append({
            "filename": filePath,
            "ai_predictions": ai_result
        })
            
    
    with open(args.o, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)



if __name__ == "__main__":
    main()