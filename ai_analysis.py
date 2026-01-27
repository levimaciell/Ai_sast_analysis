import argparse
import json
import os
import time
from ai_callers import GeminiCaller, ChatGptCaller

MAX_TRIES = 5
RETRY_DELAY = 5

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

def getAiCaller(ai, apiKey):
    callers = {
        "gemini": GeminiCaller(apiKey),
        "chat_gpt": ChatGptCaller(apiKey)
    }

    try:
        return callers[ai]
    
    except Exception:
        print(f"Erro ao tentar pegar caller da IA. Utilize os callers disponíveis: {", ".join(callers.keys())}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Executa IA como assistente SAST em todos os arquivos python que existirem em um diretório")

    parser.add_argument("-sc", required=True, help="Diretório contendo o código fonte para a IA avaliar")
    parser.add_argument("-l", required=True, help="Arquivo json contendo a análise feita pela ferramenta de sast")
    parser.add_argument("-k", required=True, help="Chave da API do Gemini")
    parser.add_argument("-o", required=True, help="Caminho do output gerado pela IA")
    parser.add_argument("-ai", required=True, help="Nome da IA a ser utilizada")

    args = parser.parse_args()

    Caller = getAiCaller(args.ai, args.k)

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
    for root, _, files in os.walk(args.sc):
        for file in files:
            if file.endswith(".py") and os.path.basename(file) in arquivosComLabel :
                filesToProcess.append(os.path.join(root,file))

    total = len(filesToProcess)
    results = []
    errors = []
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

        print(f"\n[{processed}/{total}] 🔹 Chamando IA para: {filePath} ...")
        
        success = False
        last_error = None
        raw = None

        for attempt in range(1, MAX_TRIES, + 1):
            try:
                print(f"🔁 Tentativa {attempt}/{MAX_TRIES}")

                raw = Caller.requestAi(prompt) 

                ai_result = json.loads(raw)
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
            print(f"❌ Falha definitiva em {filePath}\n")
            errors.append({
                "filename": filePath,
                "error": last_error,
                "raw": raw
            })
            continue
        else:
            results.append({
            "filename": filePath,
            "ai_predictions": ai_result
        })
            
    
    with open(args.o, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n🎯 Concluído! {processed}/{total} arquivos processados.")

    if errors:
        print(f"⚠️ Ocorreram {len(errors)} erros. Veja: erro_ia_log.json")
        with open("erro_ia_log.json", "w", encoding="utf-8") as ef:
            json.dump(errors, ef, indent=2, ensure_ascii=False)
    else:
        print("✅ Nenhum erro detectado durante as requisições à IA.")


if __name__ == "__main__":
    main()