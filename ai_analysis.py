import argparse
import json
import os
import time
from ai_callers import GeminiCaller, ChatGptCaller, DeepseekCaller, ClaudeCaller
from config import settings

MAX_TRIES = settings.MAX_RETRY_ATTEMPTS
RETRY_DELAY = settings.RETRY_DELAY_SECONDS
BASE_DIRECTORY = settings.BASE_DIRECTORY
HALLUCIONATION_FILTER = settings.HALLUCINATION_FILTER

def build_prompt(vul_code: str, vuln_sast_list: list[str]) -> str:
    example_return =  '''
    [
      {
        "label": "CWE-XXX",
        "line_of_code": <integer>
      }
    ]
    '''

    prompt =  f'''
<objective>
    Your goal is NOT to discover new vulnerabilities.
    Your goal is ONLY to validate whether the vulnerabilities reported by a SAST tool listed below are actually present in the given source code.
</objective>

<rules>
    - Use ONLY the provided source code as evidence.
    - Use ONLY the vulnerabilities listed below. Do NOT add, infer, or suggest new CWEs.
    - A vulnerability should be reported only if it is clearly supported by the source code.
    - If none of the listed vulnerabilities are confirmed, return an empty JSON array: [].
    - Output must be valid JSON only.
</rules>

<expected_output>

{example_return}

</expected_output>

<source_code>

{vul_code}

</source_code>

<sast_vulnerabilities>

{vuln_sast_list}

</sast_vulnerabilities>
'''

    return prompt



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
            labels.append(item)

        prompt = build_prompt(code, json.dumps(labels))
        
        success = False
        last_error = None

        for attempt in range(1, MAX_TRIES, + 1):
            try:

                ai_result = Caller.requestAi(prompt)

                if(HALLUCIONATION_FILTER):
                    filteredResult = []

                    for obj in ai_result:
                        cweList = []
                        for item in labels:
                            cweList.append(item['cwe'])

                        if obj['label'] in cweList:
                            filteredResult.append(obj)
                        else:
                            print(f"HALLUCINATION DETECTED! NOT ADDING RESULT TO THE .json FILE")
                            print(f'Lista original: {labels}')
                            print(f'Lista da IA: {ai_result}')


                    ai_result = filteredResult
                 
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