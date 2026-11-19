#!/usr/bin/env python3
"""Roteiro noturno: publica UMA nova subclasse CNAE da fila priorizada (scripts/content.py: FILA).

Atualiza data/processed/publicadas.json, reconstrói o site e registra em data/processed/nightly_log.jsonl.
"""
import json, subprocess, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import content as C  # noqa: E402
import build as B  # noqa: E402

TZ = ZoneInfo("America/Sao_Paulo")
LOG = ROOT / "data/processed/nightly_log.jsonl"


def main():
    pub = B.load_pub()
    feitos = {p["codigo"] for p in pub}
    agora = datetime.now(TZ)
    prox = next((f for f in C.FILA if f[0] not in feitos and f[0] in B.SUB), None)
    entry = {"quando": agora.strftime("%d/%m/%Y %H:%M") + " (horário de Brasília, UTC-3)"}
    if prox is None:
        entry.update(status="fila_vazia", titulo="", href="")
        print("Fila vazia: nenhuma atividade nova para publicar.")
    else:
        cod, curto, setor, notas = prox
        pub.append({"codigo": cod, "data": agora.strftime("%d/%m/%Y"), "origem": "noturno"})
        B.PUB_FILE.write_text(json.dumps(pub, ensure_ascii=False, indent=1), encoding="utf-8")
        href = f"cnae/{B.cnae_slug(cod, curto)}/"
        entry.update(status="publicada", codigo=cod, titulo=f"{curto} (CNAE {cod})", href=href,
                     analise_especifica=bool(notas), restantes=sum(1 for f in C.FILA if f[0] not in feitos) - 1)
        print(f"Nova atividade: {curto} (CNAE {cod}) -> {href}")
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
