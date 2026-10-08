# Projeto G1 — Desmatamento e Preservação Ambiental no Brasil

**Autor:** Marcelo Barbosa de Oliveira Junior<br>
**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python<br>
**Tema 19 • Base simulada de 2015 a 2024**

## Objetivo
Analisar a evolução do desmatamento, comparar regiões, estados e biomas e investigar preservação e relação com queimadas. Trabalho da avaliação G1 sobre o Tema 19. O documento do tema usa o título G2, mas aqui a identificação segue a avaliação G1.

## Estrutura
```text
avaliacaog1/                # raiz do projeto
├── app.py
├── analise.py              # preparação e indicadores compartilhados
├── requirements.txt
├── README.md
├── index.html
├── dados/
│   └── simulacao_desmatamento_brasil.csv
├── database/               # reservado conforme estrutura obrigatória; banco não utilizado
├── notebooks/
│   └── analise_desmatamento.ipynb
└── imagens/                # gráficos gerados pelo notebook
```

## Executar
Use Python 3.12. A partir da raiz do projeto:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
No Windows, a ativação é `.venv\Scripts\activate`.
O CSV é carregado por caminho relativo ao código, independentemente da pasta do terminal.

## Notebook
Abra `notebooks/analise_desmatamento.ipynb` em um ambiente Jupyter com as dependências de `requirements.txt` instaladas e execute todas as células em ordem. O notebook contém as dez etapas, resultados executados e figuras; pode ser visualizado diretamente no GitHub. Jupyter é uma ferramenta de execução, não uma dependência do dashboard. As figuras são regeneradas em `imagens/`.

## Requisitos atendidos
- Python, Pandas, Matplotlib, Seaborn e Streamlit da orientação G1; Plotly exigido pelo Tema 19; NumPy permitido na análise estatística.
- Seis filtros: ano, mês, região, estado, bioma e nível de risco. As opções são dependentes dos filtros anteriores; seleção vazia resulta em aviso.
- KPIs dinâmicos, análise temporal, comparação regional e por bioma, ranking estadual, heatmap mensal, dispersão, interpretação e conclusão executiva.
- Avançadas: **dashboard multipágina** e **correlação estatística de Pearson**.
- Páginas: visão geral, evolução temporal, correlação ambiental e exploração dos dados, com tabela dinâmica.
- Sem APIs, mapas ou persistência em banco: não são necessários para as duas funcionalidades avançadas escolhidas.

## Tratamento e limitações
CSV original preservado. Datas e números convertidos, categorias normalizadas, duplicatas exatas removidas e linhas inválidas contabilizadas. A base fornecida contém 4.440 registros, sem ausentes ou duplicatas exatas. Não se assume que mês/UF/bioma seja uma chave única.
A base é simulada e inclui combinações geográficas não representativas. Somar área preservada e unidades de conservação entre meses pode duplicar estoques. A soma preservada é exibida como soma de registros, com ressalva; análises de preservação usam médias. A unidade de CO₂ não foi especificada. Correlação é descritiva, não causal. Rankings absolutos não são taxas territoriais.

## Publicação e entrega
1. Envie os arquivos para o GitHub mantendo o CSV, notebook e imagens no repositório.
2. GitHub Pages: em **Settings → Pages**, escolha **Deploy from a branch**, branch `main` e pasta `/ (root)`. A apresentação está em `index.html`, na raiz.
3. Streamlit Community Cloud: entre com GitHub, crie o app, selecione este repositório, branch `main`, arquivo `app.py` e Python 3.12. As dependências vêm de `requirements.txt`.
4. Depois do deploy, adicione o URL verdadeiro do dashboard no campo “Dashboard publicado” de `index.html` e neste README. Não há URL fictício no projeto.

### Links de entrega
- Repositório atual: https://github.com/marcelobarbosa-dev/avaliacaog1
- GitHub Pages: **aguardando ativação**. Endereço esperado, após ativação: https://marcelobarbosa-dev.github.io/avaliacaog1/
- Streamlit: **aguardando deploy**.
- Notebook: `notebooks/analise_desmatamento.ipynb`.
- Dashboard: `app.py`, com apoio de `analise.py`.
- Base: `dados/simulacao_desmatamento_brasil.csv`.

