# Reforma Tributária por Atividade

Diretório estático (pt-BR) da reforma tributária do consumo (EC 132/2023, LC 214/2025) organizado por subclasse CNAE 2.3,
para ME, EPP e MEI. Mantido pela MM Consultoria Corporativa Ltda. (CNPJ 49.399.582/0001-10).

- `scripts/process_cnae.py` – lê a tabela oficial CNAE-Subclasses 2.3 (IBGE) de `data/raw/` e gera `data/processed/cnae_subclasses.json`.
- `scripts/content.py` – conteúdo verificado (artigos da LC 214, Simples, cronograma) e a fila noturna priorizada (`FILA`).
- `scripts/build.py` – gera `site/` (home, check-up, aviso legal, privacidade, metodologia, atividades, páginas CNAE, sitemap, robots).
- `nightly.py` – adiciona UMA subclasse da fila por execução (`data/processed/publicadas.json`, log em `nightly_log.jsonl`).
- `publish_nightly.sh` – roda o nightly, reconstrói, commita em `main` e publica `site/` no branch `gh-pages` (log em `publish_log.jsonl`).

Publicado em https://advogadomarciopinheiro-cmd.github.io/reforma-tributaria-micro/

Para baixar os dados brutos de novo:
`curl -LO https://ftp.ibge.gov.br/Informacoes_Gerais_e_Referencia/Classificacoes/CNAE/cnae2_3/cnae_subclasses_2_3_xls.zip` em `data/raw/` e descompactar.
Conteúdo informativo; não é consultoria individual.
