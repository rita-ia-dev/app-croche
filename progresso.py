import json
import os

ARQUIVO = "progresso.json"


def salvar_progresso(projeto, etapa):
    dados = {}

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)

    dados[projeto] = etapa

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)



def carregar_progresso():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}