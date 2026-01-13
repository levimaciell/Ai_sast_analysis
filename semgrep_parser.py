import argparse
import json
import os
import re

def extract_cwe(cwe_list):
    """
    Pega o primeiro item da lista de CWE e extrai apenas CWE-XXX.
    """
    if not cwe_list:
        return "UNKNOWN"
    
    match = re.search(r"(CWE-\d+)", cwe_list[0])
    return match.group(1) if match else "UNKNOWN"

def main():
    parser = argparse.ArgumentParser(
        description="Converte Json de output do bandit para um formato padronizado"
    )

    parser.add_argument(
        "-i", "--input", required=True,
        help="Arquivo JSON de entrada (output do Bandit)"
    )
    parser.add_argument(
        "-o", "--output", default="bandit_labels.json",
        help="Arquivo JSON de saída (default: bandit_labels.json)"
    )

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        semgrep_data = json.load(f)

    labels = []
    seen_files = set()

    for issue in semgrep_data.get("results", []):

        filename = os.path.basename(issue.get("path"))
        line = issue.get("start").get("line")

        metadata = issue.get("extra").get("metadata")
        cweId = extract_cwe(metadata.get("cwe"))

        cweFormatada = f"{line}({cweId})"

        if filename in seen_files:
            item = next(
                (d for d in labels if d["filename"] == filename),
                None
            )

            if(item):
                item["labels"].append(cweFormatada)
            else:
                raise Exception("Inconsistency found. the file is in seen files but the dict was not availiable")

        else:            
            fileInfo = {
                "filename": filename,
                "labels": [cweFormatada]
            }

            labels.append(fileInfo)

        seen_files.add(filename)
    
    print(f"Total de arquivos escaneados: {len(semgrep_data.get("paths").get("scanned"))}")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()