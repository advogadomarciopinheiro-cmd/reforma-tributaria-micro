#!/usr/bin/env python3
"""Gera o site estático em ./site a partir de data/processed e scripts/content.py."""
import html, json, os, re, shutil, sys, unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import content as C  # noqa: E402

BASE = os.environ.get("BASE_URL", "/reforma-tributaria-micro/")
SITE_URL = os.environ.get("SITE_URL", "https://advogadomarciopinheiro-cmd.github.io/reforma-tributaria-micro").rstrip("/")
OUT = ROOT / "site"
SUB = json.loads((ROOT / "data/processed/cnae_subclasses.json").read_text(encoding="utf-8"))
PUB_FILE = ROOT / "data/processed/publicadas.json"

SITE_NOME = "Reforma Tributária por Atividade"
EMPRESA = "MM Consultoria Corporativa Ltda."
CNPJ = "49.399.582/0001-10"
EMAIL = "solucoescorporativasmm@gmail.com"
PRECO = "R$ 200"
AFILIADOS = []  # preencher quando houver contas: [{"nome":..., "url":..., "texto":..., "setores":[...]}]

e = html.escape
TZ = ZoneInfo("America/Sao_Paulo")


def hoje():
    return datetime.now(TZ).strftime("%d/%m/%Y")


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def cnae_slug(cod, den):
    return slugify(cod.replace("/", "-")) + "-" + slugify(den)


def url(path=""):
    return BASE + path.lstrip("/")


def abs_url(path=""):
    return SITE_URL + "/" + path.lstrip("/")


def fonte_link(key):
    s = C.SRC[key]
    return f'<a href="{e(s["url"])}" rel="noopener" target="_blank">{e(s["nome"])}</a>'


def mailto(assunto, cnae_txt=""):
    corpo = (
        "Olá, quero o Check-up da Reforma Tributária (R$ 200).\n\n"
        f"Atividade / CNAE: {cnae_txt}\n"
        "Regime atual (MEI, Simples, Lucro Presumido ou Real):\n"
        "Vendo mais para empresas, para consumidor final ou para os dois?\n"
        "Cidade/UF:\n\n"
        "Não envie dados sensíveis nem documentos agora.\n\n"
        "CONSENTIMENTO (obrigatório): autorizo a MM Consultoria Corporativa Ltda. (CNPJ 49.399.582/0001-10) "
        "a usar meu nome, e-mail e as informações acima apenas para responder este pedido e enviar a proposta do Check-up. "
        "Posso revogar a qualquer momento respondendo REVOGAR.\n\n"
        "Novidades por e-mail (opcional, consentimento separado): escreva SIM aqui se quiser receber: ___\n"
    )
    return f"mailto:{EMAIL}?subject={quote(assunto)}&body={quote(corpo)}"


CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#1d2433;--muted:#5b6475;--brand:#0f5b4f;--brand2:#e8f3f0;--warn:#fff5e0;--warnb:#e0a100;--line:#e3e6ec}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--brand)}a:hover{text-decoration:none}
.wrap{max-width:960px;margin:0 auto;padding:0 16px}
header.top{background:#fff;border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;padding-top:12px;padding-bottom:12px}
.logo{font-weight:700;color:var(--ink);text-decoration:none;font-size:1.05rem}.logo span{color:var(--brand)}
nav a{margin-right:14px;text-decoration:none;color:var(--muted);font-size:.95rem}nav a.cta{color:#fff;background:var(--brand);padding:6px 12px;border-radius:6px;margin-right:0}
main{padding:24px 0 40px}
h1{font-size:1.7rem;line-height:1.25;margin:.2em 0 .5em}h2{font-size:1.25rem;margin:1.6em 0 .5em}h3{font-size:1.05rem}
.lead{font-size:1.1rem;color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0}
.grid{display:grid;grid-template-columns:1fr;gap:12px}
@media(min-width:640px){.grid{grid-template-columns:1fr 1fr}h1{font-size:2rem}}
@media(min-width:900px){.grid.g3{grid-template-columns:1fr 1fr 1fr}}
.grid a.card{display:block;text-decoration:none;color:var(--ink);margin:0}.grid a.card:hover{border-color:var(--brand)}
.tag{display:inline-block;font-size:.78rem;background:var(--brand2);color:var(--brand);padding:2px 8px;border-radius:99px;margin-bottom:6px}
.alert{background:var(--warn);border-left:4px solid var(--warnb);padding:12px 16px;border-radius:6px;margin:16px 0}
.cta-box{background:var(--brand);color:#fff;border-radius:10px;padding:18px 20px;margin:24px 0}.cta-box a.btn{background:#fff;color:var(--brand)}
.cta-box p{margin:.3em 0}
a.btn{display:inline-block;background:var(--brand);color:#fff;text-decoration:none;padding:10px 16px;border-radius:8px;font-weight:600;margin-top:8px}
.small{font-size:.88rem;color:var(--muted)}.cta-box .small{color:#d9efe9}
table{width:100%;border-collapse:collapse;font-size:.95rem}td,th{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left;vertical-align:top}
.pend{display:inline-block;font-size:.75rem;background:#fde8e8;color:#9b1c1c;padding:1px 7px;border-radius:99px}
.crumbs{font-size:.85rem;color:var(--muted)}.crumbs a{color:var(--muted)}
ul.src li{margin:.3em 0}
.ad-slot{border:1px dashed var(--line);border-radius:8px;padding:12px;margin:20px 0;background:#fff}
.ad-slot .label{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
footer{border-top:1px solid var(--line);background:#fff;padding:20px 0;font-size:.88rem;color:var(--muted)}
footer a{color:var(--muted);margin-right:12px}
"""


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def page(path, title, desc, body, extra_ld=None, crumbs=None):
    canon = abs_url(path)
    crumbs_html = ""
    if crumbs:
        crumbs_html = '<div class="crumbs">' + " › ".join(
            f'<a href="{url(p)}">{e(n)}</a>' if p is not None else e(n) for n, p in crumbs) + "</div>"
    lds = "".join(ld(x) for x in (extra_ld or []))
    doc = f"""<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canon)}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(canon)}"><meta property="og:locale" content="pt_BR">
<link rel="stylesheet" href="{url('assets/style.css')}">
{lds}
</head><body>
<header class="top"><div class="wrap">
<a class="logo" href="{url()}">Reforma <span>por Atividade</span></a>
<nav><a href="{url('atividades/')}">Atividades</a><a href="{url('metodologia/')}">Fontes</a><a class="cta" href="{url('check-up/')}">Check-up {PRECO}</a></nav>
</div></header>
<main><div class="wrap">{crumbs_html}
{body}
</div></main>
<footer><div class="wrap">
<p><strong>{EMPRESA}</strong> · CNPJ {CNPJ} · Assessoria corporativa e consultoria tributária. Conteúdo informativo, sem vínculo com a Receita Federal, o CGIBS ou outros órgãos públicos.</p>
<p><a href="{url('check-up/')}">Check-up</a><a href="{url('aviso-legal/')}">Aviso legal</a><a href="{url('privacidade/')}">Privacidade</a><a href="{url('metodologia/')}">Metodologia e fontes</a><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Este site não usa cookies nem ferramentas de rastreamento.</p>
</div></footer>
</body></html>"""
    dest = OUT / path / "index.html" if not path.endswith(".html") else OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    return canon


def ad_slot(setor=None):
    # Espaço reservado para links de afiliado (CONAR: rótulo "Publicidade"). Vazio enquanto AFILIADOS = [].
    itens = [a for a in AFILIADOS if not a.get("setores") or setor in a.get("setores", [])]
    if not itens:
        return "<!-- espaço de Publicidade reservado: sem anunciantes no momento -->"
    lis = "".join(f'<li><a href="{e(a["url"])}" rel="sponsored noopener" target="_blank">{e(a["nome"])}</a> — {e(a["texto"])}</li>' for a in itens)
    return f'<aside class="ad-slot"><div class="label">Publicidade</div><ul>{lis}</ul><p class="small">Podemos receber comissão se você contratar por estes links. Isso não muda o conteúdo informativo das páginas.</p></aside>'


def urgencia_box():
    u = C.URGENCIA
    fontes = " · ".join(fonte_link(k) for k in u["fontes"])
    return f'<div class="alert"><strong>Prazo real:</strong> {e(u["texto"])}<br><span class="small">{e(u["dado"])} Fontes: {fontes}. Consultado em {C.CONSULTA}.</span></div>'


def cta_box(cnae_txt=""):
    assunto = "Check-up da Reforma Tributária" + (f" - CNAE {cnae_txt}" if cnae_txt else "")
    return f"""<div class="cta-box"><p><strong>Check-up da Reforma Tributária por {PRECO}</strong></p>
<p>Um diagnóstico educacional da sua empresa: Simples (DAS) x Simples híbrido x regime regular, impacto para a sua atividade, premissas e fontes. Não substitui o seu contador.</p>
<a class="btn" href="{e(mailto(assunto, cnae_txt))}">Pedir o check-up por e-mail</a> <a class="btn" href="{url('check-up/')}">Ver escopo e limites</a>
<p class="small">O botão abre seu e-mail com um texto pronto. Ao enviar, você autoriza o uso dos dados só para responder ao pedido (<a style="color:#fff" href="{url('privacidade/')}">privacidade</a>).</p></div>"""


def load_pub():
    if PUB_FILE.exists():
        return json.loads(PUB_FILE.read_text(encoding="utf-8"))
    data = [{"codigo": c, "data": hoje(), "origem": "inicial"} for c in C.INICIAIS]
    PUB_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


def meta_for(cod):
    if cod in C.INICIAIS:
        m = C.INICIAIS[cod]
        return m["curto"], m["setor"], m["tratamento"], m.get("b2b"), True
    for c, curto, setor, notas in C.FILA:
        if c == cod:
            return curto, setor, (notas or C.GENERICO_TRATAMENTO), None, bool(notas)
    raise KeyError(cod)


def cnae_page(item):
    cod = item["codigo"]
    s = SUB[cod]
    den = s["denominacao"]
    curto, setor, trat, b2b, especifico = meta_for(cod)
    slug = cnae_slug(cod, curto)
    path = f"cnae/{slug}/"
    title = f"Reforma tributária para {curto.lower()} (CNAE {cod}) — o que muda no Simples"
    desc = f"CNAE {cod} – {den}: IBS, CBS, Simples Nacional, regime híbrido, créditos e cronograma 2026–2033, com artigos da LC 214/2025 e fontes oficiais."
    trat_html = "".join(f"<li>{e(t)} <span class='small'>[{fonte_link(k)}]</span></li>" for t, k in trat)
    if not especifico:
        trat_html += "<li><span class='pend'>análise específica pendente</span> A leitura desta atividade com seus produtos e serviços é feita no check-up.</li>"
    simples = "".join(f"<li>{e(t)}</li>" for t in C.SIMPLES_BASE)
    crono = "".join(f"<tr><th>{e(a)}</th><td>{e(t)}</td></tr>" for a, t in C.CRONOGRAMA)
    b2b_txt = b2b or C.B2B_BASE
    body = f"""
<span class="tag">{e(setor)}</span>
<h1>Reforma tributária: {e(curto)} <small class="small">(CNAE {e(cod)})</small></h1>
<p class="lead">O que a reforma do consumo (EC 132/2023 e LC 214/2025) muda para microempresas, empresas de pequeno porte e MEIs desta atividade.</p>
{urgencia_box()}
<h2>Descrição oficial da subclasse</h2>
<div class="card"><p><strong>{e(cod)} — {e(den)}</strong></p>
<p class="small">Seção {e(s['secao'])}: {e(s['secao_nome'] or '')} · Divisão {e(s['divisao'])}: {e(s['divisao_nome'] or '')} · Grupo {e(s['grupo'])}: {e(s['grupo_nome'] or '')} · Classe {e(s['classe'])}: {e(s['classe_nome'] or '')}</p>
<p class="small">Fonte: {fonte_link('cnae')}. Consultado em {C.CONSULTA}. Para saber o que a subclasse inclui e exclui, consulte as notas explicativas da CONCLA/IBGE.</p></div>
<h2>Tratamento diferenciado na LC 214/2025</h2>
<ul>{trat_html}</ul>
<p class="small"><span class="pend">depende de regulamentação</span> {e(C.PENDENTE_ALIQUOTA)}</p>
<h2>O que muda para quem está no Simples Nacional</h2>
<ul>{simples}</ul>
<p class="small">Fontes: {fonte_link('prsn')}; {fonte_link('lc214')}; {fonte_link('manual')}.</p>
<h2>Vende para empresas ou para consumidor final? Créditos</h2>
<p>{e(b2b_txt)}</p>
<p class="small">Base: LC 214, arts. 47 e 41. {fonte_link('lc214')}</p>
<h2>Split payment</h2>
<p>A LC 214 prevê que o IBS e a CBS sejam separados e recolhidos no momento da liquidação financeira do pagamento (split payment), em procedimento padrão ou simplificado opcional (arts. 31 a 35, com redação da LC 227/2026). <span class="pend">depende de regulamentação</span> O cronograma de implantação para cada meio de pagamento depende de regulamentação.</p>
<h2>Cronograma da transição</h2>
<table>{crono}</table>
<p class="small">Fontes: {fonte_link('lc214')}; {fonte_link('ec132')}. Consultado em {C.CONSULTA}.</p>
{cta_box(cod + ' ' + den)}
{ad_slot(setor)}
<p class="small">Página publicada em {e(item.get('data', hoje()))}. Conteúdo informativo, não é consultoria individual nem garante economia de tributos. Leia o <a href="{url('aviso-legal/')}">aviso legal</a>. Encontrou um erro? Escreva para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
"""
    lds = [{
        "@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
        "inLanguage": "pt-BR", "datePublished": _iso(item.get("data")), "dateModified": _iso(hoje()),
        "author": {"@type": "Organization", "name": EMPRESA}, "publisher": {"@type": "Organization", "name": EMPRESA},
        "mainEntityOfPage": abs_url(path), "about": f"CNAE {cod} {den}"},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": abs_url("")},
            {"@type": "ListItem", "position": 2, "name": "Atividades", "item": abs_url("atividades/")},
            {"@type": "ListItem", "position": 3, "name": f"CNAE {cod}", "item": abs_url(path)}]}]
    page(path, title, desc, body, lds, crumbs=[("Início", ""), ("Atividades", "atividades/"), (f"CNAE {cod}", None)])
    return {"codigo": cod, "den": den, "curto": curto, "setor": setor, "path": path, "data": item.get("data")}


def _iso(d):
    try:
        return datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m-%d")
    except Exception:
        return datetime.now(TZ).strftime("%Y-%m-%d")


def cards(pages):
    return '<div class="grid g3">' + "".join(
        f'<a class="card" href="{url(p["path"])}"><span class="tag">{e(p["setor"])}</span><br><strong>{e(p["curto"])}</strong><br><span class="small">CNAE {e(p["codigo"])} — {e(p["den"])}</span></a>'
        for p in pages) + "</div>"


def home(pages):
    org = {"@context": "https://schema.org", "@type": "Organization", "name": EMPRESA, "taxID": CNPJ,
           "email": EMAIL, "url": abs_url(""), "description": "Assessoria corporativa e consultoria tributária para micro e pequenas empresas."}
    web = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NOME, "url": abs_url(""), "inLanguage": "pt-BR"}
    body = f"""
<h1>A reforma tributária explicada pela sua atividade (CNAE)</h1>
<p class="lead">IBS, CBS, Simples Nacional, regime híbrido e créditos: o que muda para ME, EPP e MEI, atividade por atividade, só com fontes oficiais e o artigo da lei citado.</p>
{urgencia_box()}
<h2>Escolha sua atividade</h2>
{cards(pages[-9:][::-1] if len(pages) > 9 else pages)}
<p><a href="{url('atividades/')}">Ver todas as {len(pages)} atividades →</a> <span class="small">Uma atividade nova é publicada toda noite.</span></p>
<h2>O essencial em 4 pontos</h2>
<div class="grid">
<div class="card"><h3>1. Novos tributos</h3><p>A CBS (federal) e o IBS (estados e municípios) substituem PIS, Cofins, ICMS e ISS aos poucos, até 2033. O Imposto Seletivo incide sobre itens como bebidas alcoólicas e açucaradas.</p></div>
<div class="card"><h3>2. Simples continua</h3><p>A partir de 2027, IBS e CBS entram no DAS por padrão. A empresa do Simples pode optar por recolhê-los por fora (híbrido) em setembro ou março. O MEI não tem essa opção.</p></div>
<div class="card"><h3>3. Crédito virou argumento de venda</h3><p>Clientes empresariais no regime regular descontam o imposto pago nas compras. Isso pode pesar na escolha do regime de quem vende para empresas.</p></div>
<div class="card"><h3>4. Alíquotas finais ainda não fixadas</h3><p>As alíquotas de referência dependem de fixação futura. Aqui marcamos o que está confirmado e o que <span class="pend">depende de regulamentação</span>.</p></div>
</div>
{cta_box()}
<h2>Fontes oficiais usadas</h2>
<ul class="src"><li>{fonte_link('lc214')}</li><li>{fonte_link('ec132')}</li><li>{fonte_link('prsn')}</li><li>{fonte_link('cnae')}</li><li>{fonte_link('fato')}</li><li>{fonte_link('cgibs')}</li></ul>
<p class="small">Site da {EMPRESA}, assessoria corporativa e consultoria tributária. Não somos órgão público nem escritório de contabilidade.</p>
"""
    page("", f"{SITE_NOME}: IBS, CBS e Simples Nacional por CNAE", "Guia da reforma tributária do consumo por atividade (CNAE) para ME, EPP e MEI: Simples, regime híbrido, créditos, prazos e fontes oficiais.", body, [org, web])


def atividades(pages):
    by = {}
    for p in pages:
        by.setdefault(p["setor"], []).append(p)
    body = "<h1>Atividades (CNAE) publicadas</h1><p class='lead'>Cada página explica a reforma para uma subclasse da CNAE 2.3. Uma nova é publicada toda noite.</p>"
    for setor in sorted(by):
        body += f"<h2>{e(setor)}</h2>" + cards(by[setor])
    page("atividades/", "Atividades por CNAE — reforma tributária para ME, EPP e MEI", "Lista de atividades (CNAE 2.3) com o que muda na reforma tributária do consumo para micro e pequenas empresas.", body,
         crumbs=[("Início", ""), ("Atividades", None)])


def checkup():
    svc = {"@context": "https://schema.org", "@type": "Service", "name": "Check-up da Reforma Tributária",
           "provider": {"@type": "Organization", "name": EMPRESA, "taxID": CNPJ, "email": EMAIL},
           "areaServed": "BR", "serviceType": "Diagnóstico educacional sobre a reforma tributária do consumo",
           "offers": {"@type": "Offer", "price": "200.00", "priceCurrency": "BRL", "url": abs_url("check-up/")}}
    body = f"""
<h1>Check-up da Reforma Tributária — {PRECO}</h1>
<p class="lead">Um diagnóstico educacional, por escrito, de como a reforma do consumo afeta a sua empresa, com premissas e fontes explicadas.</p>
{urgencia_box()}
<h2>O que está incluído</h2>
<ul>
<li>Comparação entre <strong>Simples (DAS)</strong>, <strong>Simples híbrido</strong> (IBS e CBS por fora) e <strong>regime regular</strong>, em cenários, para o seu caso.</li>
<li>Leitura dos dispositivos da LC 214/2025 aplicáveis à sua atividade (CNAE) e aos principais produtos ou serviços que você vende.</li>
<li>Análise do seu perfil de clientes (empresas x consumidor final) e do efeito dos créditos de IBS e CBS.</li>
<li>Calendário dos prazos que importam para você, como a janela de março de 2027.</li>
<li>Relatório com premissas, limites e links para as fontes oficiais.</li>
</ul>
<h2>O que não está incluído</h2>
<ul>
<li>Escrituração contábil ou fiscal, emissão de guias (inclusive DAS), entrega de declarações e alteração de regime nos portais.</li>
<li>Substituição do seu contador. Essas atividades são de profissional registrado no Conselho Regional de Contabilidade (CRC).</li>
<li>Parecer jurídico, representação perante órgãos públicos ou defesa em processos.</li>
<li>Garantia de economia de tributos. O resultado depende dos seus dados e da regulamentação ainda pendente.</li>
</ul>
<h2>Premissas</h2>
<ul>
<li>A análise usa os dados informados por você e a legislação vigente na data do relatório.</li>
<li>As alíquotas de referência do IBS e da CBS ainda não foram fixadas. Por isso trabalhamos com cenários e deixamos explícito o que <span class="pend">depende de regulamentação</span>.</li>
<li>A decisão final sobre o regime é sua, de preferência junto com o seu contador.</li>
</ul>
<h2>Como contratar</h2>
<ol>
<li>Clique em “Pedir o check-up por e-mail”. Seu e-mail abre com um texto pronto: preencha a atividade, o regime atual e o perfil de clientes. Não envie documentos nem dados sensíveis nessa etapa.</li>
<li>Respondemos com a proposta: escopo, prazo de entrega e forma de pagamento. Nada é cobrado antes do seu aceite.</li>
<li>Depois do aceite e do pagamento, pedimos as informações necessárias e entregamos o relatório por e-mail.</li>
</ol>
<p class="small">Na contratação a distância, você pode desistir em até 7 dias (Código de Defesa do Consumidor, art. 49). Preço: {PRECO} por empresa (um CNPJ).</p>
{cta_box()}
<p class="small">Prestador: {EMPRESA}, CNPJ {CNPJ}, assessoria corporativa e consultoria tributária. Contato: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
"""
    page("check-up/", f"Check-up da Reforma Tributária por {PRECO} — ME, EPP e MEI", "Diagnóstico educacional da reforma tributária para micro e pequenas empresas: Simples x híbrido x regular, impacto por CNAE, premissas e fontes. R$ 200.", body, [svc],
         crumbs=[("Início", ""), ("Check-up", None)])


def aviso():
    body = f"""
<h1>Aviso legal</h1>
<p>Este site é mantido pela {EMPRESA} (CNPJ {CNPJ}), que atua em assessoria corporativa e consultoria tributária.</p>
<h2>Conteúdo informativo</h2>
<p>As páginas têm caráter informativo e educacional. Elas resumem a legislação e as orientações oficiais e não são consultoria individual, parecer jurídico ou serviço contábil. Situações concretas dependem de dados e documentos que estas páginas não analisam.</p>
<h2>Sem garantia de resultado</h2>
<p>Não prometemos nem garantimos economia de tributos ou qualquer resultado financeiro. A reforma ainda depende de regulamentação, e as regras podem mudar depois da data de cada página.</p>
<h2>Fontes e atualização</h2>
<p>Usamos só fontes oficiais, citadas com link e data de consulta em cada página (veja <a href="{url('metodologia/')}">metodologia</a>). Se encontrar erro ou desatualização, escreva para <a href="mailto:{EMAIL}">{EMAIL}</a> e corrigimos.</p>
<h2>Sem vínculo com órgãos públicos</h2>
<p>Este site não é da Receita Federal, do Comitê Gestor do IBS, do Comitê Gestor do Simples Nacional, do IBGE ou de qualquer órgão público e não fala em nome deles.</p>
<h2>Serviços contábeis</h2>
<p>Escrituração, emissão de guias e entrega de declarações são atividades de profissional registrado no CRC e não são prestadas por meio deste site.</p>
<h2>Publicidade</h2>
<p>Se houver anúncios ou links de afiliado, eles aparecerão identificados com o rótulo “Publicidade”, como recomenda o CONAR. Hoje o site não tem anunciantes.</p>
"""
    page("aviso-legal/", "Aviso legal — Reforma Tributária por Atividade", "Conteúdo informativo, sem consultoria individual e sem garantia de economia. Responsável: MM Consultoria Corporativa Ltda.", body,
         crumbs=[("Início", ""), ("Aviso legal", None)])


def privacidade():
    body = f"""
<h1>Política de privacidade</h1>
<p class="small">Atualizada em {hoje()}.</p>
<h2>Quem é a controladora</h2>
<p>{EMPRESA}, CNPJ {CNPJ}. Contato para assuntos de privacidade: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Quais dados tratamos</h2>
<p>O site não tem formulário, não usa cookies e não usa ferramentas de análise ou rastreamento. Só tratamos os dados que você nos envia por e-mail: nome, endereço de e-mail e as informações que escrever, como atividade, regime e cidade.</p>
<p>A hospedagem (GitHub Pages) pode registrar dados técnicos de acesso, como o endereço IP, para segurança e funcionamento do serviço, conforme a política do próprio GitHub.</p>
<h2>Para que usamos e com qual base legal</h2>
<ul>
<li><strong>Responder seu pedido e enviar a proposta do Check-up:</strong> com base no seu consentimento (LGPD, art. 7º, I), dado ao enviar o e-mail com o texto de consentimento.</li>
<li><strong>Prestar o serviço contratado:</strong> execução de contrato (LGPD, art. 7º, V), só se você contratar.</li>
<li><strong>Enviar novidades sobre a reforma:</strong> só com consentimento separado e opcional (escrevendo SIM no campo indicado). Você pode pedir o check-up sem aceitar novidades.</li>
</ul>
<h2>Compartilhamento</h2>
<p>Não vendemos nem cedemos seus dados. O e-mail é operado pelo provedor do nosso endereço (Google/Gmail), que atua como operador.</p>
<h2>Por quanto tempo guardamos</h2>
<p>Pelo tempo necessário para responder o pedido e prestar o serviço, ou até você revogar o consentimento. Depois disso, mantemos apenas o que a lei exigir.</p>
<h2>Seus direitos e como revogar</h2>
<p>Você pode pedir confirmação, acesso, correção, eliminação e informações sobre o uso dos seus dados (LGPD, art. 18). Para revogar o consentimento, responda qualquer e-mail nosso com a palavra <strong>REVOGAR</strong> ou escreva para <a href="mailto:{EMAIL}?subject=REVOGAR">{EMAIL}</a>. Você também pode reclamar à Autoridade Nacional de Proteção de Dados (ANPD).</p>
<h2>Cookies</h2>
<p>Este site não usa cookies. Se isso mudar, esta política será atualizada e um aviso será exibido antes de qualquer cookie não essencial.</p>
"""
    page("privacidade/", "Política de privacidade (LGPD) — Reforma Tributária por Atividade", "Como a MM Consultoria Corporativa Ltda. trata os dados enviados por e-mail: finalidades, consentimento, revogação e direitos (LGPD).", body,
         crumbs=[("Início", ""), ("Privacidade", None)])


def metodologia():
    srcs = "".join(f"<li>{fonte_link(k)}</li>" for k in C.SRC)
    body = f"""
<h1>Metodologia e fontes</h1>
<h2>Como as páginas são feitas</h2>
<ul>
<li>A descrição e a hierarquia de cada atividade vêm da tabela oficial CNAE-Subclasses 2.3 do IBGE/CONCLA, processada automaticamente.</li>
<li>O tratamento na LC 214/2025 só é descrito quando o dispositivo foi conferido no texto compilado do Planalto. Cada afirmação cita o artigo ou o anexo.</li>
<li>Quando ainda não há análise específica, a página diz isso de forma explícita e mostra só as regras gerais.</li>
<li>O que depende de ato futuro (alíquotas de referência, regulamentação do split payment, reflexo das reduções no DAS) é marcado como <span class="pend">depende de regulamentação</span>.</li>
<li>Não publicamos alíquotas finais, simulações de valores nem estimativas de economia.</li>
</ul>
<h2>Limite importante</h2>
<p>As reduções e os regimes específicos da LC 214 se aplicam por produto ou serviço (NCM/NBS) e por tipo de operação, não pelo CNAE. O CNAE serve como porta de entrada; o enquadramento real depende do que a empresa vende.</p>
<h2>Fontes oficiais (consultadas em {C.CONSULTA})</h2>
<ul class="src">{srcs}</ul>
<h2>Atualização</h2>
<p>Uma atividade nova é publicada toda noite. As páginas são revistas quando há mudança relevante nas fontes. Correções: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
"""
    page("metodologia/", "Metodologia e fontes oficiais — Reforma Tributária por Atividade", "Como o diretório é construído: CNAE 2.3 do IBGE, LC 214/2025, EC 132/2023 e orientações da Receita e do Simples Nacional.", body,
         crumbs=[("Início", ""), ("Metodologia", None)])


def notfound():
    body = f"<h1>Página não encontrada</h1><p><a href='{url()}'>Voltar ao início</a> ou veja as <a href='{url('atividades/')}'>atividades</a>.</p>"
    page("404.html", "Página não encontrada", "Página não encontrada.", body)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    (OUT / "assets/style.css").write_text(CSS.strip(), encoding="utf-8")
    pub = load_pub()
    pages = [cnae_page(it) for it in pub]
    home(pages); atividades(pages); checkup(); aviso(); privacidade(); metodologia(); notfound()
    paths = ["", "atividades/", "check-up/", "metodologia/", "aviso-legal/", "privacidade/"] + [p["path"] for p in pages]
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{abs_url(p)}</loc><lastmod>{today}</lastmod></url>\n" for p in paths) + "</urlset>\n"
    (OUT / "sitemap.xml").write_text(sm, encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {abs_url('sitemap.xml')}\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"site gerado: {len(pages)} atividades, {len(paths)} URLs no sitemap -> {OUT}")


if __name__ == "__main__":
    main()
