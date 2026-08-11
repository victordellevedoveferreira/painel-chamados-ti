# Painel de Chamados de TI

Projeto de portfolio que simula uma operacao de suporte tecnico: geracao de dados ficticios, tratamento com Python e pandas, consultas SQL em SQLite e dashboard HTML interativo.

> Os dados sao sinteticos e reproduziveis; nao representam usuarios, equipamentos ou atendimentos reais.

**Demonstracao online:** [Abrir dashboard](https://victordellevedoveferreira.github.io/painel-chamados-ti/)

## Indicadores analisados

- volume e taxa de resolucao de chamados;
- cumprimento de SLA;
- tempo medio de resolucao;
- satisfacao dos usuarios;
- categorias e prioridades com maior demanda.

## Tecnologias

- Python 3.11, pandas e unittest
- SQLite e SQL
- HTML, CSS e JavaScript
- ETL, validacao de dados, KPIs e SLA

## Estrutura

    data/       # dados sinteticos brutos e tratados
    docs/       # dashboard e metricas exportadas
    src/        # geracao de dados, ETL, metricas e SQLite
    tests/      # testes automatizados

## Como executar

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python -m src.pipeline --regenerate
    python -m unittest discover -s tests -v
    Start-Process .\docs\index.html

## Qualidade dos dados

O pipeline valida colunas obrigatorias, datas, identificadores duplicados e tempos de resolucao negativos. Chamados ainda abertos nao entram no calculo de tempo medio nem de SLA.

## Autor

Victor Dellevedove Ferreira  
[LinkedIn](https://www.linkedin.com/in/victor-dellevedove-ferreira-114b34256/) · [GitHub](https://github.com/victordellevedoveferreira)
