import argparse
import json
import os

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
        bandit_data = json.load(f)

    labels = []
    seen_files = set()

    for issue in bandit_data.get("results", []):

        filename = os.path.basename(issue.get("filename"))
        line = issue.get("line_number")
        cweId = issue.get("issue_cwe", {}).get("id")
        cweFormatada = f"{line}(CWE-{cweId})"

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



    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()