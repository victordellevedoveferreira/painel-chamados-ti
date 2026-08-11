# Painel de Chamados de TI

Projeto de portfolio que simula a analise de uma operacao de suporte tecnico: geracao de dados ficticios, limpeza com Python e pandas, consultas SQL em SQLite e um dashboard HTML interativo.

> Os dados sao sinteticos, reproduziveis e nao representam usuarios, equipamentos ou atendimentos reais.

## Objetivo

Transformar uma base de chamados em indicadores uteis para a tomada de decisao:

- volume e taxa de resolucao;
- cumprimento de SLA;
- tempo medio de resolucao;
- satisfacao dos usuarios;
- categorias e prioridades com maior demanda.

## Tecnologias

- Python 3.11, pandas e unittest
- SQLite e SQL
- HTML, CSS e JavaScript
- ETL, validacao de dados, KPIs e SLA
- Git e GitHub

## Estrutura

    data/       # dados sinteticos brutos e tratados
    docs/       # dashboard e metricas exportadas
    src/        # geracao de dados, ETL, metricas e banco SQLite
    tests/      # testes automatizados

## Como executar

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python -m src.pipeline --regenerate
    python -m unittest discover -s tests -v
    Start-Process .\docs\index.html

## Qualidade e seguranca dos dados

O pipeline valida colunas obrigatorias, datas, identificadores duplicados e tempos de resolucao negativos. Chamados ainda abertos nao entram no calculo de tempo medio nem de SLA.

## Proximos passos

- publicar o dashboard no GitHub Pages;
- criar uma versao equivalente no Power BI;
- adicionar testes de integracao para o banco SQLite;
- incluir analise de causa raiz para chamados recorrentes.

## Autor

Victor Dellevedove Ferreira  
[LinkedIn](https://www.linkedin.com/in/victor-ferreira-114b34256) · [GitHub](https://github.com/victordellevedoveferreira)
