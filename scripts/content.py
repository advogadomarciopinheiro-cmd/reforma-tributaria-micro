"""Conteúdo editorial verificado do diretório.

Regras: só afirmar o que está no texto oficial (LC 214/2025 compilada no Planalto, EC 132/2023,
Perguntas e Respostas do Simples Nacional, Manual da Opção pelo Regime Regular e notícias oficiais).
Todas as remissões abaixo foram conferidas no texto baixado em 19/11/2026.
"""

CONSULTA = "19/11/2026"

SRC = {
    "lc214": {"nome": "Lei Complementar nº 214/2025 (texto compilado, Planalto)",
              "url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm"},
    "ec132": {"nome": "Emenda Constitucional nº 132/2023 (Planalto)",
              "url": "https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm"},
    "cnae": {"nome": "CNAE-Subclasses 2.3 — Estrutura detalhada (IBGE/CONCLA)",
             "url": "https://ftp.ibge.gov.br/Informacoes_Gerais_e_Referencia/Classificacoes/CNAE/cnae2_3/"},
    "prsn": {"nome": "Perguntas e Respostas do Simples Nacional (CGSN, atualizado parcialmente em 09/10/2026)",
             "url": "https://www8.receita.fazenda.gov.br/simplesnacional/arquivos/manual/perguntaosn.pdf"},
    "manual": {"nome": "Manual da Opção pelo Regime Regular do IBS e da CBS no Simples Nacional (Receita Federal)",
               "url": "https://www8.receita.fazenda.gov.br/simplesnacional/Arquivos/manual/Manual%20op%C3%A7%C3%A3o%20regime%20regular%20IBS%20e%20CBS%20no%20Simples%20Nacional.pdf"},
    "noticia": {"nome": "Receita Federal — notícia de 18/11/2026 sobre opções pelo Simples Nacional e pelo regime regular do IBS e da CBS",
                "url": "https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/novembro/a-receita-federal-divulga-a-atualizacao-dos-numeros-referentes-as-solicitacoes-de-opcao-pelo-simples-nacional-e-pelo-regime-regular-do-ibs-e-da-cbs"},
    "fato": {"nome": "Reforma de Fato — Receita Federal",
             "url": "https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/reforma-tributaria-do-consumo/reforma-de-fato"},
    "cgibs": {"nome": "Comitê Gestor do IBS (CGIBS)", "url": "https://www.cgibs.gov.br/"},
}

# --- Blocos comuns a todas as páginas de atividade -------------------------------------------

CRONOGRAMA = [
    ("2026", "Ano de teste: CBS de 0,9% e IBS de 0,1%, compensáveis com PIS/Cofins (LC 214, arts. 343, 346 e 348; EC 132, art. 125 do ADCT). "
             "Essas alíquotas de teste não se aplicam às operações de optantes pelo Simples Nacional (LC 214, art. 348, III, “c”)."),
    ("2027", "CBS passa a ser cobrada e PIS/Cofins são extintos; começa o Imposto Seletivo (EC 132, art. 126 do ADCT). "
             "IBS de 0,1% (0,05% estadual + 0,05% municipal) em 2027 e 2028 (LC 214, art. 344). No Simples, IBS e CBS entram no DAS, salvo opção pelo regime regular (Perguntas e Respostas do Simples, 1.6 e 2.27)."),
    ("2029–2032", "ICMS e ISS caem gradualmente: 9/10 das alíquotas em 2029, 8/10 em 2030, 7/10 em 2031 e 6/10 em 2032 (EC 132, art. 128 do ADCT)."),
    ("2033", "ICMS e ISS são extintos (EC 132, art. 129 do ADCT); IBS e CBS passam a vigorar integralmente."),
]

PENDENTE_ALIQUOTA = ("As alíquotas de referência do IBS e da CBS a partir de 2027 ainda dependem de fixação conforme a LC 214 "
                     "(arts. 345 e seguintes) e de resolução do Senado Federal. Por isso, este site não publica percentuais finais.")

SIMPLES_BASE = [
    "Por padrão, a partir de 2027 o optante pelo Simples Nacional (exceto o MEI) paga IBS e CBS “por dentro”, no DAS (Perguntas e Respostas do Simples, 2.27).",
    "A empresa do Simples pode optar por apurar IBS e CBS “por fora”, no regime regular, o chamado Simples híbrido (LC 214, art. 41, § 3º). A opção abre nos meses de setembro e março, com efeito no semestre seguinte (Perguntas e Respostas do Simples, 2.27). O MEI não tem essa opção.",
    "Quem fica no DAS não aproveita créditos de IBS e CBS nas compras (LC 214, art. 47, § 9º, I). Já o cliente que está no regime regular pode tomar crédito do valor pago pelo fornecedor do Simples, limitado ao que foi recolhido no regime único (art. 47, § 9º, II).",
    "As reduções de alíquota e os regimes específicos da LC 214 são regras do regime regular. Como eles se refletem no valor pago dentro do DAS depende da regulamentação do Simples (CGSN) — ponto ainda a confirmar caso a caso.",
]

B2B_BASE = ("Venda para empresa (B2B): se o seu cliente está no regime regular, ele pode descontar como crédito o IBS e a CBS da sua nota. "
            "Pelo DAS, esse crédito fica limitado ao que foi pago no Simples; no regime regular (híbrido), o crédito corresponde ao imposto destacado. "
            "Venda para consumidor final (B2C): o consumidor não toma crédito, então esse argumento perde força e o custo total de cada regime pesa mais. "
            "A comparação depende dos seus números e não há resultado garantido.")

URGENCIA = {
    "texto": ("Quem pediu o regime regular do IBS e da CBS para o 1º semestre de 2027 pode cancelar esse pedido de 03/11/2026 até 20/12/2026, "
              "em caráter irretratável: depois de cancelado, não dá para refazer a opção para o mesmo período. A próxima janela de opção é março de 2027, "
              "com efeito no semestre seguinte."),
    "fontes": ["manual", "noticia", "prsn"],
    "dado": "Até 18/11/2026 a Receita registrou 1.090.080 solicitações de opção pelo regime regular do IBS e da CBS e 30.370 cancelamentos.",
}

GENERICO_TRATAMENTO = [
    ("Esta página ainda não traz análise de um dispositivo da LC 214 específico para esta atividade. "
     "Os regimes diferenciados (reduções de 30%, 60% ou 100%) e os regimes específicos da lei são definidos pelo produto ou serviço "
     "(códigos NCM/NBS dos anexos) ou pelo tipo de operação — não pelo CNAE. Ter este CNAE não garante nem exclui uma redução.",
     "lc214"),
]

# --- 7 páginas iniciais (conteúdo verificado) ------------------------------------------------

INICIAIS = {
    "5611-2/01": {
        "curto": "Restaurantes",
        "setor": "Alimentação",
        "tratamento": [
            ("Bares e restaurantes, inclusive lanchonetes, têm regime específico de IBS e CBS (LC 214, art. 273). Ele também vale para bebidas não alcoólicas preparadas no estabelecimento (art. 273, § 1º).", "lc214"),
            ("Ficam fora desse regime: alimentação para pessoa jurídica sob contrato ou fornecida por empresa da subclasse 5620-1/01; produtos e bebidas não alcoólicas revendidos sem preparo; e bebidas alcoólicas, mesmo preparadas na casa (art. 273, § 2º).", "lc214"),
            ("As alíquotas do IBS e da CBS desse regime são reduzidas em 40% (art. 275).", "lc214"),
            ("Saem da base de cálculo a gorjeta repassada integralmente ao empregado, até 15% da conta, e os valores retidos pela plataforma de delivery que não chegam ao restaurante (art. 274, parágrafo único).", "lc214"),
            ("Quem compra refeições de bares e restaurantes não pode tomar crédito de IBS e CBS (art. 276).", "lc214"),
        ],
        "b2b": ("Como o cliente empresarial não toma crédito sobre refeições de restaurante (art. 276), a vantagem do regime regular em vendas B2B é bem menor nesta atividade. "
                "Para quem vende principalmente ao consumidor final, a comparação Simples (DAS) x híbrido tende a girar em torno do custo total."),
        "buscas": "imposto restaurante reforma tributária, IBS CBS restaurante Simples Nacional",
    },
    "4120-4/00": {
        "curto": "Construção de edifícios",
        "setor": "Construção",
        "tratamento": [
            ("Operações com bens imóveis feitas por contribuintes do regime regular seguem regime específico (LC 214, art. 251). Entre elas estão os serviços de construção civil, a alienação (inclusive por incorporação e parcelamento de solo), a locação e a administração e intermediação (art. 252, I a V).", "lc214"),
            ("As alíquotas de IBS e CBS dessas operações são reduzidas em 50%; na locação, cessão onerosa e arrendamento, em 70% (art. 261).", "lc214"),
            ("Na venda de imóveis há ainda redutores de ajuste e redutor social (arts. 257 a 260) e regras próprias para incorporação imobiliária (Seção V do mesmo capítulo). O cálculo depende do caso concreto.", "lc214"),
        ],
        "b2b": ("Obras para empresas do regime regular permitem ao contratante tomar crédito do IBS e da CBS destacados na nota. "
                "Por isso, quem constrói para empresas costuma ter mais motivo para comparar o Simples (DAS) com o regime regular do que quem atende só pessoas físicas."),
        "buscas": "reforma tributária construção civil Simples, IBS CBS obra empreiteira",
    },
    "9602-5/01": {
        "curto": "Salão de beleza",
        "setor": "Beleza",
        "tratamento": [
            ("Na leitura do texto compilado da LC 214 feita em 19/11/2026, não localizamos regime específico nem redução de alíquota voltados a serviços de cabeleireiro, manicure e pedicure. Em princípio, aplica-se a alíquota padrão, que ainda não foi fixada.", "lc214"),
            ("Produtos de higiene pessoal e limpeza listados no Anexo VIII têm redução de 60% (art. 128, VII). Isso vale para a venda desses produtos, não para o serviço do salão.", "lc214"),
        ],
        "b2b": ("Salões atendem quase sempre o consumidor final (B2C), que não toma crédito. Assim, o argumento do crédito para o cliente pesa pouco, e a comparação Simples (DAS) x híbrido gira em torno do custo total e do volume de compras com crédito."),
        "buscas": "reforma tributária salão de beleza, IBS CBS cabeleireiro MEI",
    },
    "6201-5/01": {
        "curto": "Software sob encomenda",
        "setor": "Tecnologia",
        "tratamento": [
            ("Na leitura do texto compilado da LC 214 feita em 19/11/2026, não localizamos regime específico nem redução de alíquota voltados ao desenvolvimento de software sob encomenda. Em princípio, aplica-se a alíquota padrão, que ainda não foi fixada.", "lc214"),
            ("Exportações de serviços para o exterior são imunes ao IBS e à CBS, mantido o direito aos créditos das aquisições (art. 79; o conceito de exportação de serviço está no art. 80).", "lc214"),
        ],
        "b2b": ("Software sob encomenda costuma ser vendido para empresas. Se os clientes estão no regime regular, eles podem tomar crédito do IBS e da CBS da sua nota. "
                "É um dos perfis em que a comparação entre DAS e regime regular (híbrido) mais merece atenção."),
        "buscas": "reforma tributária empresa de software Simples, IBS CBS TI desenvolvedor",
    },
    "4712-1/00": {
        "curto": "Minimercado e mercearia",
        "setor": "Comércio varejista",
        "tratamento": [
            ("No comércio, a tributação depende de cada produto (código NCM), não do CNAE da loja.", "lc214"),
            ("Os itens da Cesta Básica Nacional do Anexo I, como arroz, feijão, leite, carnes e pão francês, têm alíquota zero (art. 125). Hortícolas, frutas e ovos do Anexo XV têm redução de 100%.", "lc214"),
            ("Os alimentos do Anexo VII têm redução de 60% (art. 128, VI), assim como os produtos de higiene pessoal e limpeza do Anexo VIII (art. 128, VII).", "lc214"),
            ("Bebidas alcoólicas e açucaradas estão no campo do Imposto Seletivo (art. 409, § 1º, IV e V).", "lc214"),
        ],
        "b2b": ("A venda é quase toda para o consumidor final (B2C). O que pesa é o cadastro correto do NCM de cada produto, para aplicar a alíquota certa a partir de 2027, e a comparação do custo total entre DAS e regime regular."),
        "buscas": "reforma tributária mercadinho Simples, cesta básica alíquota zero IBS CBS",
    },
    "4930-2/02": {
        "curto": "Transporte rodoviário de carga",
        "setor": "Transporte",
        "tratamento": [
            ("Na leitura do texto compilado da LC 214 feita em 19/11/2026, não localizamos redução de alíquota para o transporte rodoviário de carga. O regime específico da lei (arts. 284 a 286) trata do transporte coletivo de passageiros.", "lc214"),
            ("Quem contrata frete de transportador autônomo pessoa física não contribuinte pode, no regime regular, apropriar crédito presumido (art. 169).", "lc214"),
            ("Veículos de transporte de carga destinados a transportador autônomo de carga têm alíquota zero na aquisição, nas condições da lei (art. 110, II).", "lc214"),
        ],
        "b2b": ("O frete é quase sempre contratado por empresas. Embarcadores no regime regular podem tomar crédito do IBS e da CBS do frete. "
                "Para transportadoras, a escolha entre DAS e regime regular (híbrido) pode afetar diretamente a competitividade do preço."),
        "buscas": "reforma tributária transportadora Simples, IBS CBS frete",
    },
    "8630-5/03": {
        "curto": "Clínica médica (consultas)",
        "setor": "Saúde",
        "tratamento": [
            ("Os serviços de saúde do Anexo III têm redução de 60% nas alíquotas de IBS e CBS (LC 214, arts. 128, II, e 130). Entre eles estão os serviços de clínica médica (item 7, NBS 1.2301.21.00) e os serviços médicos especializados (item 8, NBS 1.2301.22.00).", "lc214"),
            ("Não entram na base de cálculo os valores glosados pela auditoria médica de planos de saúde e não pagos (art. 130, parágrafo único).", "lc214"),
        ],
        "b2b": ("Consultas são pagas sobretudo por pessoas físicas e planos de saúde. Para pacientes pessoas físicas (B2C) não há crédito. A comparação entre DAS e regime regular deve considerar a redução de 60%, que é uma regra do regime regular, e o perfil de quem paga."),
        "buscas": "reforma tributária clínica médica Simples, IBS CBS saúde redução 60%",
    },
}

# --- Fila noturna priorizada (uma subclasse por noite) -----------------------------------
# Cada item: código CNAE 2.3, rótulo curto, setor e, quando verificado no texto, observações.

def _rest(extra=None):
    base = [("Bares e restaurantes, inclusive lanchonetes, têm regime específico de IBS e CBS com redução de 40% nas alíquotas (LC 214, arts. 273 e 275). Bebidas alcoólicas e produtos revendidos sem preparo ficam fora desse regime (art. 273, § 2º), e o cliente não toma crédito (art. 276).", "lc214")]
    return base + (extra or [])

SAUDE = lambda item, nome, nbs: [(f"Os serviços de saúde do Anexo III têm redução de 60% nas alíquotas de IBS e CBS (LC 214, arts. 128, II, e 130). O item {item} do anexo é “{nome}” (NBS {nbs}).", "lc214")]
CONSTR = [("Os serviços de construção civil estão entre as operações com bens imóveis do regime específico (LC 214, art. 252, V), com redução de 50% para contribuintes do regime regular (arts. 251 e 261). O enquadramento do serviço deve ser confirmado pela classificação NBS.", "lc214")]
IMOV = [("A administração e a intermediação de imóveis estão no regime específico de operações com bens imóveis (LC 214, art. 252, IV), com redução de 50% para contribuintes do regime regular (arts. 251 e 261).", "lc214")]
PROF = lambda prof: [(f"A LC 214 reduz em 30% as alíquotas de IBS e CBS de serviços de {prof} sujeitos a conselho profissional (art. 127). Para pessoa jurídica valem requisitos cumulativos, como sócios habilitados, nenhum sócio pessoa jurídica e serviços prestados pelos próprios sócios (art. 127, § 1º, II).", "lc214")]

FILA = [
    ("5611-2/03", "Lanchonete", "Alimentação", _rest()),
    ("9602-5/02", "Estética", "Beleza", None),
    ("4781-4/00", "Loja de roupas", "Comércio varejista", None),
    ("4520-0/01", "Oficina mecânica", "Serviços automotivos", None),
    ("8630-5/04", "Odontologia", "Saúde", SAUDE(9, "Serviços odontológicos", "1.2301.23.00")),
    ("4399-1/03", "Obras de alvenaria", "Construção", CONSTR),
    ("7020-4/00", "Consultoria em gestão", "Serviços profissionais", None),
    ("4721-1/02", "Padaria (revenda)", "Alimentação", [("No comércio de alimentos, a tributação depende de cada produto (NCM). O pão francês e sua pré-mistura estão na Cesta Básica Nacional, com alíquota zero (LC 214, art. 125, Anexo I, item 16).", "lc214")]),
    ("8650-0/04", "Fisioterapia", "Saúde", SAUDE(11, "Serviços de fisioterapia", "1.2301.92.00")),
    ("4744-0/99", "Material de construção", "Comércio varejista", None),
    ("6920-6/01", "Contabilidade", "Serviços profissionais", PROF("contabilistas")),
    ("4771-7/01", "Farmácia", "Comércio varejista", [("Medicamentos registrados na Anvisa têm redução de 60% (LC 214, art. 133), e os medicamentos do Anexo XIV têm alíquota zero (art. 146).", "lc214")]),
    ("4321-5/00", "Instalação elétrica", "Construção", CONSTR),
    ("5620-1/04", "Marmitas e comida para casa", "Alimentação", None),
    ("6204-0/00", "Consultoria em TI", "Tecnologia", None),
    ("8650-0/03", "Psicologia", "Saúde", SAUDE(17, "Serviços de psicologia", "1.2301.98.00")),
    ("4930-2/01", "Frete municipal", "Transporte", [("Quem contrata frete de transportador autônomo pessoa física não contribuinte pode, no regime regular, apropriar crédito presumido (LC 214, art. 169).", "lc214")]),
    ("9313-1/00", "Academia", "Serviços pessoais", None),
    ("4772-5/00", "Cosméticos e perfumaria", "Comércio varejista", [("Os produtos de higiene pessoal e limpeza do Anexo VIII têm redução de 60% (LC 214, art. 128, VII). A tributação de cada item depende do NCM.", "lc214")]),
    ("6821-8/01", "Corretagem de imóveis", "Imobiliário", IMOV),
    ("8121-4/00", "Limpeza predial e residencial", "Serviços", None),
    ("1091-1/02", "Padaria (produção própria)", "Alimentação", [("O pão francês e sua pré-mistura estão na Cesta Básica Nacional, com alíquota zero (LC 214, art. 125, Anexo I, item 16). Os demais produtos dependem do NCM.", "lc214")]),
    ("7311-4/00", "Agência de publicidade", "Serviços", None),
    ("8640-2/02", "Laboratório clínico", "Saúde", SAUDE(12, "Serviços laboratoriais", "1.2301.93.00")),
    ("4724-5/00", "Hortifrúti", "Comércio varejista", [("Hortícolas, frutas e ovos listados no Anexo XV têm redução de 100% nas alíquotas de IBS e CBS (LC 214, Anexo XV).", "lc214")]),
    ("4722-9/01", "Açougue", "Comércio varejista", [("Carnes bovina, suína, ovina, caprina e de aves dos códigos NCM listados estão na Cesta Básica Nacional, com alíquota zero (LC 214, art. 125, Anexo I, item 19).", "lc214")]),
    ("5611-2/04", "Bar", "Alimentação", _rest()),
    ("6203-1/00", "Software de prateleira/SaaS", "Tecnologia", None),
    ("5320-2/02", "Entregas rápidas (motoboy)", "Transporte", None),
    ("8599-6/04", "Treinamentos", "Educação", None),
    ("4723-7/00", "Loja de bebidas", "Comércio varejista", [("Bebidas alcoólicas e bebidas açucaradas estão no campo do Imposto Seletivo (LC 214, art. 409, § 1º, IV e V).", "lc214")]),
    ("7500-1/00", "Veterinária", "Saúde animal", PROF("médicos veterinários")),
    ("9609-2/08", "Banho e tosa", "Pet", None),
    ("4789-0/04", "Pet shop", "Comércio varejista", None),
    ("5510-8/01", "Hotel e pousada", "Hospedagem", [("Os serviços de hotelaria têm regime específico com redução de 40% nas alíquotas de IBS e CBS (LC 214, arts. 277 e 281), e o cliente não toma crédito (art. 283).", "lc214")]),
    ("8650-0/02", "Nutrição", "Saúde", SAUDE(22, "Serviços de nutrição", "1.2301.99.00")),
    ("8650-0/06", "Fonoaudiologia", "Saúde", SAUDE(21, "Serviços de fonoaudiologia", "1.2301.99.00")),
    ("8650-0/01", "Enfermagem", "Saúde", SAUDE(10, "Serviços de enfermagem", "1.2301.91.00")),
    ("7111-1/00", "Arquitetura", "Serviços profissionais", PROF("arquitetos e urbanistas")),
    ("7112-0/00", "Engenharia", "Serviços profissionais", PROF("engenheiros")),
    ("6822-6/00", "Administração de imóveis", "Imobiliário", IMOV),
    ("4330-4/04", "Pintura de edifícios", "Construção", CONSTR),
    ("4782-2/01", "Loja de calçados", "Comércio varejista", None),
    ("4751-2/01", "Loja de informática", "Comércio varejista", None),
    ("9511-8/00", "Assistência técnica de computadores", "Serviços", None),
    ("4530-7/03", "Autopeças", "Comércio varejista", None),
    ("4520-0/05", "Lava-jato", "Serviços automotivos", None),
    ("8593-7/00", "Escola de idiomas", "Educação", None),
    ("8211-3/00", "Serviços de escritório", "Serviços", None),
    ("4729-6/99", "Comércio de alimentos em geral", "Comércio varejista", None),
    ("1412-6/01", "Confecção de roupas", "Indústria", None),
    ("4754-7/01", "Loja de móveis", "Comércio varejista", None),
    ("4744-0/01", "Ferragens e ferramentas", "Comércio varejista", None),
    ("4774-1/00", "Ótica", "Comércio varejista", None),
    ("8230-0/01", "Organização de eventos e festas", "Serviços", None),
    ("7420-0/01", "Fotografia", "Serviços", None),
    ("9601-7/01", "Lavanderia", "Serviços", None),
    ("4924-8/00", "Transporte escolar", "Transporte", None),
    ("4923-0/01", "Táxi", "Transporte", None),
    ("4511-1/02", "Revenda de carros usados", "Comércio varejista", None),
    ("4761-0/03", "Papelaria", "Comércio varejista", None),
    ("4763-6/01", "Loja de brinquedos", "Comércio varejista", None),
    ("6319-4/00", "Portais e conteúdo na internet", "Tecnologia", None),
    ("7319-0/02", "Promoção de vendas", "Serviços", None),
    ("8630-5/02", "Clínica médica com exames", "Saúde", SAUDE(7, "Serviços de clínica médica", "1.2301.21.00")),
]
