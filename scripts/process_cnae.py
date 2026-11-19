#!/usr/bin/env python3
"""Lê a tabela oficial CNAE-Subclasses 2.3 (IBGE/CONCLA) e gera data/processed/cnae_subclasses.json."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
XLS = ROOT / "data/raw/CNAE-Subclasses 2_3 - Estrutura Detalhada.xls"
OUT = ROOT / "data/processed/cnae_subclasses.json"

def main():
    df = pd.read_excel(XLS, header=None, dtype=str)
    cur = {"secao": None, "divisao": None, "grupo": None, "classe": None}
    names = {}
    out = {}
    for _, r in df.iloc[4:].iterrows():
        sec, div, gru, cla, sub, den = [(x.strip() if isinstance(x, str) else None) for x in r.tolist()[:6]]
        if not den or den in ("Denominação", "(continua)", "(conclusão)") or sec == "Seção":
            continue
        if sec and not (len(sec) == 1 and sec.isalpha()):
            continue
        den = " ".join(den.split())
        if sec:
            cur.update(secao=sec, divisao=None, grupo=None, classe=None); names[("secao", sec)] = den
        elif div:
            cur.update(divisao=div, grupo=None, classe=None); names[("divisao", div)] = den
        elif gru:
            cur.update(grupo=gru, classe=None); names[("grupo", gru)] = den
        elif cla:
            cur.update(classe=cla); names[("classe", cla)] = den
        elif sub:
            out[sub] = {
                "codigo": sub,
                "denominacao": den,
                "secao": cur["secao"], "secao_nome": names.get(("secao", cur["secao"])),
                "divisao": cur["divisao"], "divisao_nome": names.get(("divisao", cur["divisao"])),
                "grupo": cur["grupo"], "grupo_nome": names.get(("grupo", cur["grupo"])),
                "classe": cur["classe"], "classe_nome": names.get(("classe", cur["classe"])),
            }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} subclasses -> {OUT}")

if __name__ == "__main__":
    main()
