# Desmatamento e Preservação Ambiental no Brasil
Aluno : Marcelo Barbosa de Oliveira Junior
Professor: Alexandre Louzada
Matéria: Linguagens de Programação

## 1. Descrição do projeto

Este projeto analisa uma base simulada de desmatamento no Brasil entre 2015 e 2024. O trabalho inclui leitura e tratamento dos dados, análise exploratória, indicadores, gráficos e um dashboard interativo.

Foi desenvolvido para a avaliação **G1** da disciplina **Linguagem de Programação — Análise e Visualização de Dados com Python**, sobre o **Tema 19**.

**Aluno:** Marcelo Barbosa de Oliveira Junior.

### Fluxo do projeto

```text
simulacao_desmatamento_brasil.csv (base fornecida pelo professor)
    ↓ Leitura e preparação com Pandas
analise.py (dados tratados em memória, sem alterar o CSV original)
    ↓ Análise e visualizações
analise_desmatamento.ipynb + imagens/
    ↓ Dashboard com filtros e indicadores
app.py (Streamlit)
    ↓ Publicação
GitHub + GitHub Pages + Streamlit Community Cloud
```

---

## 2. Problema da análise

O desmatamento pode afetar a biodiversidade, os recursos hídricos e o equilíbrio ambiental. Neste trabalho, a base simulada é usada para responder:

- Quais estados apresentam maior área desmatada?
- Quais biomas são mais afetados?
- Como o desmatamento evoluiu entre 2015 e 2024?
- Existem anos ou meses com maiores totais?
- Há relação entre queimadas e desmatamento?
- Quais regiões têm maior área preservada média por registro?
- Como a preservação varia ao longo do tempo?

**Sobre a base:** são 4.440 registros, 14 colunas originais, cinco regiões, 20 UFs e seis biomas. Os dados são simulados e não representam estatísticas oficiais do Brasil.

---

## 3. Tecnologias utilizadas

| Tecnologia | Função |
|------------|--------|
| Python | Linguagem principal |
| Pandas | Leitura, tratamento e análise dos dados |
| Matplotlib | Gráficos estáticos do notebook |
| Seaborn | Visualizações estatísticas do notebook |
| Plotly | Gráficos interativos do dashboard |
| NumPy | Biblioteca numérica utilizada no ambiente de análise |
| Streamlit | Dashboard interativo e multipágina |
| Git/GitHub | Versionamento e armazenamento do código |
| GitHub Pages | Publicação da página HTML |
| Streamlit Community Cloud | Publicação do dashboard |

As duas funcionalidades avançadas escolhidas são **dashboard multipágina** e **correlação estatística**. O projeto não utiliza banco de dados; a pasta `database/` foi mantida para seguir a estrutura exigida.

---

## 4. Estrutura do projeto

```text
avaliacaog1/
│
├── app.py                         # Dashboard Streamlit
├── analise.py                     # Preparação e cálculo dos indicadores
├── requirements.txt               # Dependências
├── README.md                      # Apresentação e instruções
├── index.html                     # Página do projeto
│
├── dados/
│   └── simulacao_desmatamento_brasil.csv
│
├── database/
│   └── .gitkeep                    # Pasta reservada, sem banco utilizado
│
├── notebooks/
│   └── analise_desmatamento.ipynb
│
└── imagens/                        # Gráficos gerados pelo notebook
```

---

## 5. Como executar localmente

Use **Python 3.12**.

### 5.1 Clonar o repositório

```bash
git clone https://github.com/marcelobarbosa-dev/avaliacaog1.git
cd avaliacaog1
```

### 5.2 Instalar as dependências

É recomendado criar um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Depois, instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### 5.3 Executar o dashboard

```bash
python -m streamlit run app.py
```

### 5.4 Executar o notebook

Abra `notebooks/analise_desmatamento.ipynb` em um ambiente Jupyter ou no VS Code com suporte a notebooks. Selecione um ambiente Python com as dependências instaladas e execute as células na ordem.

O notebook já está salvo com os resultados. Ao executá-lo novamente, os gráficos são gerados na pasta `imagens/`. Jupyter precisa estar disponível no ambiente usado para abrir o notebook; não é uma dependência do dashboard.

---

## 6. KPIs utilizados

| KPI | Descrição |
|-----|-----------|
| Área total desmatada | Soma da área desmatada nos registros, em km² |
| Área preservada registrada | Soma das observações de área preservada, em km² |
| Bioma mais afetado | Bioma com maior soma de área desmatada |
| Estado mais crítico | Estado com maior soma de área desmatada |
| Total de queimadas | Soma dos focos de queimada |
| Emissões de CO₂ | Soma das emissões estimadas na base |

A área preservada pode estar repetida entre meses. Por isso, sua soma **não representa território único**; nas comparações e na evolução da preservação, também são usadas médias por registro. A unidade das emissões de CO₂ não foi informada na base.

---

## 7. Funcionalidades do dashboard

- Filtros por ano, mês, região, estado, bioma e nível de risco.
- KPIs que mudam conforme os filtros.
- Gráficos de evolução mensal e anual do desmatamento.
- Comparação entre regiões, estados e biomas.
- Heatmap mensal para observar sazonalidade.
- Dispersão de queimadas e desmatamento.
- Matriz de correlação de Pearson.
- Evolução da área preservada média por registro.
- Tabela dinâmica com agrupamento selecionável e tabela dos registros filtrados.
- Interpretação dos resultados e conclusão em cada página.
- Aviso quando os filtros não retornam registros.

### Páginas do dashboard

| Página | Conteúdo |
|--------|----------|
| Visão geral | KPIs, comparação regional, rankings e áreas críticas |
| Evolução temporal | Séries mensais e anuais, variação percentual e heatmap |
| Correlação ambiental | Dispersão e correlação entre indicadores |
| Exploração dos dados | Qualidade da base, tabela dinâmica e dados filtrados |

Os filtros são dependentes: as opções disponíveis consideram as seleções anteriores. Uma seleção vazia não retorna dados.

---

## 8. Notebook de análise

O arquivo `notebooks/analise_desmatamento.ipynb` contém as dez etapas exigidas:

| Etapa | Conteúdo |
|-------|----------|
| 1. Introdução ao problema | Contexto ambiental e objetivo do trabalho |
| 2. Explicação da base | Fonte, colunas, cobertura e limitações |
| 3. Leitura dos dados | Importação do CSV com Pandas |
| 4. Limpeza e preparação | Conversão de tipos, validação, ausentes e duplicatas |
| 5. Engenharia de atributos | Trimestre, período mensal, risco elevado e variação anual |
| 6. Análise exploratória | Distribuições e quantidade de registros por grupo |
| 7. KPIs | Cálculo dos indicadores ambientais |
| 8. Gráficos | Linhas, barras, heatmap, dispersão e correlação |
| 9. Interpretação dos resultados | Respostas às perguntas da análise |
| 10. Conclusão | Resultados principais e limites do estudo |

O tratamento preserva o CSV original. São normalizadas categorias, convertidas datas e números, verificadas inconsistências e contabilizadas exclusões. Na base fornecida, não foram encontrados valores ausentes, duplicatas exatas ou registros inválidos pelas regras implementadas.

---

## 9. Principais resultados

Na base completa, sem filtros:

- A soma da área desmatada é **314.603,65 km²**.
- **RJ** apresenta a maior soma de área desmatada entre os estados.
- **Mata Atlântica** apresenta a maior soma entre os biomas.
- O maior total anual ocorre em **2017**.
- Entre 2015 e 2024 há leve redução da soma anual, de aproximadamente **0,21%**, com oscilações intermediárias.
- A correlação de Pearson entre queimadas e desmatamento é aproximadamente **−0,0076**, indicando associação linear muito fraca nesta simulação.

Os resultados mudam conforme os filtros. Rankings absolutos dependem da quantidade e composição dos registros, e não representam taxas territoriais. A base contém combinações de estado e bioma que podem não representar a geografia real. Correlação não demonstra causalidade.

---

## 10. Publicação

| Entrega | Plataforma | Link |
|---------|------------|------|
| Código-fonte | GitHub | [Repositório](https://github.com/marcelobarbosa-dev/avaliacaog1) |
| Página do projeto | GitHub Pages | [Apresentação](https://marcelobarbosa-dev.github.io/avaliacaog1/) |
| Dashboard | Streamlit Community Cloud | [Dashboard interativo](https://avaliacaog1-5wn5vknc8mnh352pp9oqci.streamlit.app/) |

### Arquivos para entrega

- [Notebook de análise](notebooks/analise_desmatamento.ipynb).
- [Código do dashboard](app.py).
- [Preparação e indicadores](analise.py).
- [Base de dados utilizada](dados/simulacao_desmatamento_brasil.csv).

Para configurar o GitHub Pages, selecione **Settings → Pages → Deploy from a branch → main → / (root)**. No Streamlit Community Cloud, use a branch `main`, o arquivo `app.py` e Python 3.12.

---

## 11. Objetivo pedagógico

Praticar o uso de Python para organizar e analisar dados, criar indicadores e gráficos e apresentar os resultados em um dashboard e em uma página HTML.

Mais do que gerar gráficos, o trabalho busca responder às perguntas propostas e explicar os resultados com cuidado. Como a base é simulada, conclusões sobre o Brasil real exigiriam dados oficiais e documentação adequada.
