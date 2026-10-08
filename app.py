from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from analise import carregar, indicadores, numero, ranking

st.set_page_config(page_title="G1 | Desmatamento no Brasil", layout="wide")
@st.cache_data
def dados():
    return carregar()
base, qualidade = dados()
st.sidebar.title("Projeto G1")
st.sidebar.caption("Marcelo Barbosa de Oliveira Junior")
st.sidebar.header("Filtros do recorte")
df = base.copy()
for coluna, titulo in [("ano", "Ano"), ("mes", "Mês"), ("regiao", "Região"), ("uf", "Estado"), ("bioma", "Bioma"), ("nivel_risco", "Nível de risco")]:
    opcoes = sorted(df[coluna].dropna().unique().tolist())
    selecao = st.sidebar.multiselect(titulo, opcoes, default=opcoes, key=coluna)
    df = df[df[coluna].isin(selecao)]
st.sidebar.caption(f"{len(df):,} de {len(base):,} registros. Opções dependem dos filtros anteriores. Seleção vazia não retorna dados.")

NOTA = "Base simulada fornecida pelo professor (2015–2024). Resultados representam registros da simulação, não estatísticas oficiais. A soma de área preservada pode contar a mesma área em diferentes meses; não representa território único. A unidade de CO₂ não foi informada na base."

def cabecalho(subtitulo):
    st.title("Desmatamento e Preservação Ambiental no Brasil")
    st.caption("G1 • Linguagem de Programação — Análise e Visualização de Dados com Python")
    st.markdown("**Autor:** Marcelo Barbosa de Oliveira Junior")
    st.write(subtitulo)
    st.info(NOTA)
    if df.empty:
        st.warning("Não há registros para os filtros selecionados. Amplie o recorte na barra lateral.")
        st.stop()

def grafico(fig):
    fig.update_layout(template="plotly_white", margin=dict(l=15,r=15,t=55,b=20))
    st.plotly_chart(fig, width="stretch")

def resumo():
    cabecalho("Investigar a evolução do desmatamento, comparar estados e biomas e observar indicadores ambientais entre 2015 e 2024.")
    k = indicadores(df)
    for col, (titulo, valor) in zip(st.columns(3), [("Área desmatada (km²)",numero(k["desmatamento"])),("Área preservada — soma dos registros (km²)",numero(k["preservacao"])),("Focos de queimada",numero(k["queimadas"],0))]):
        col.metric(titulo,valor)
    for col, (titulo, valor) in zip(st.columns(3), [("Emissões de CO₂ — unidade não informada",numero(k["co2"])),("Bioma mais afetado",k["bioma"]),("Estado com maior soma desmatada",k["estado"])]):
        col.metric(titulo,valor)
    st.subheader("Comparação regional")
    regional = df.groupby("regiao", as_index=False).agg(desmatamento=("area_desmatada_km2","sum"),preservada_media=("area_preservada_km2","mean"),registros=("uf","size"))
    grafico(px.bar(regional.sort_values("desmatamento",ascending=False),x="regiao",y="desmatamento",title="Área desmatada por região",labels={"regiao":"Região","desmatamento":"Área desmatada (km²)"},color="regiao"))
    st.dataframe(regional, hide_index=True, width="stretch")
    st.caption("Média de preservação por registro permite comparar regiões sem somar estoques mensais; ainda depende da composição da simulação.")
    st.subheader("Estados e biomas")
    for coluna, titulo in [("uf","Estado"),("bioma","Bioma")]:
        r=ranking(df,coluna).rename("area_desmatada_km2").reset_index()
        grafico(px.bar(r,x=coluna,y="area_desmatada_km2",title=f"Ranking por {titulo.lower()}",labels={coluna:titulo,"area_desmatada_km2":"Área desmatada (km²)"}))
    st.subheader("Interpretação do recorte")
    elevados = df[df.risco_elevado].area_desmatada_km2.sum()
    st.write(f"{k['estado']} lidera a soma desmatada, e {k['bioma']} é o bioma mais afetado no recorte. Registros classificados como Alto ou Crítico acumulam {numero(elevados)} km². Rankings absolutos dependem da quantidade de observações por grupo; não medem taxas territoriais.")
    st.subheader("Áreas críticas e preservação")
    criticas=df[df.risco_elevado].groupby(["regiao","uf","bioma"],as_index=False).agg(area_desmatada_km2=("area_desmatada_km2","sum"),registros=("ano","size"))
    st.dataframe(criticas.sort_values("area_desmatada_km2",ascending=False), hide_index=True)
    preservacao=df.groupby("regiao").area_preservada_km2.mean().sort_values(ascending=False)
    st.write(f"A região {preservacao.index[0]} apresenta a maior área preservada média por registro: {numero(preservacao.iloc[0])} km². O número de unidades de conservação é um estoque: usamos médias, sem interpretar somas mensais como unidades distintas.")
    st.dataframe(df.groupby("regiao",as_index=False).agg(unidades_conservacao_media=("unidades_conservacao","mean")),hide_index=True)
    st.subheader("Conclusão executiva")
    st.write("O recorte identifica concentrações para investigação e períodos que merecem acompanhamento. Priorizar estados e biomas com maiores somas e registros de risco elevado é uma hipótese de monitoramento da simulação. Decisões reais exigem bases oficiais, cobertura territorial comparável e definição das unidades de emissão.")

def temporal():
    cabecalho("Evolução mensal e anual, sazonalidade e preservação ambiental.")
    mensal=df.groupby("data",as_index=False).agg(area_desmatada_km2=("area_desmatada_km2","sum"),preservada_media=("area_preservada_km2","mean"))
    grafico(px.line(mensal,x="data",y="area_desmatada_km2",markers=True,title="Evolução mensal do desmatamento",labels={"data":"Mês","area_desmatada_km2":"Área desmatada (km²)"}))
    anual=df.groupby("ano",as_index=False).area_desmatada_km2.sum()
    anual["variacao_percentual"] = anual.area_desmatada_km2.pct_change(fill_method=None)*100
    grafico(px.bar(anual,x="ano",y="area_desmatada_km2",title="Desmatamento anual",labels={"ano":"Ano","area_desmatada_km2":"Área desmatada (km²)"}))
    st.dataframe(anual,hide_index=True)
    st.caption("Variação calculada entre anos selecionados; anos ou meses incompletos não devem ser comparados como anos inteiros.")
    matriz=df.pivot_table(index="ano",columns="mes",values="area_desmatada_km2",aggfunc="sum").reindex(columns=range(1,13))
    grafico(px.imshow(matriz,aspect="auto",color_continuous_scale="YlOrRd",title="Heatmap mensal — área desmatada",labels=dict(x="Mês",y="Ano",color="km²")))
    grafico(px.line(mensal,x="data",y="preservada_media",title="Evolução da área preservada média por registro",labels={"data":"Mês","preservada_media":"Média por registro (km²)"}))
    pico=mensal.loc[mensal.area_desmatada_km2.idxmax()]
    st.write(f"O mês com maior soma desmatada no recorte é {pico['data']:%m/%Y}, com {numero(pico['area_desmatada_km2'])} km². O mapa de calor permite localizar concentrações sazonais, sem estabelecer causas.")
    if len(anual)>1:
        primeiro,ultimo=anual.iloc[0],anual.iloc[-1]
        variacao=(ultimo.area_desmatada_km2/primeiro.area_desmatada_km2-1)*100 if primeiro.area_desmatada_km2 else None
        if variacao is not None:
            st.write(f"Entre {int(primeiro.ano)} e {int(ultimo.ano)}, a variação das somas selecionadas foi de {numero(variacao)}%. Há oscilações intermediárias; compare períodos com a mesma cobertura.")
    st.subheader("Conclusão executiva")
    st.write("Monitorar picos mensais e a evolução anual ajuda a definir períodos de atenção. A preservação é apresentada como média por registro para evitar interpretar observações repetidas como área única.")

def correlacoes():
    cabecalho("Relação entre queimadas, desmatamento, chuva, temperatura e emissões estimadas.")
    grafico(px.scatter(df,x="focos_queimada",y="area_desmatada_km2",color="bioma",hover_data=["ano","mes","uf"],opacity=.45,title="Queimadas × desmatamento",labels={"focos_queimada":"Focos de queimada","area_desmatada_km2":"Área desmatada (km²)","bioma":"Bioma"}))
    cols=["area_desmatada_km2","focos_queimada","chuva_mm","temperatura_media","emissoes_co2","area_preservada_km2"]
    matriz=df[cols].corr(method="pearson")
    grafico(px.imshow(matriz,zmin=-1,zmax=1,color_continuous_scale="RdBu_r",text_auto=".2f",aspect="auto",title="Correlação de Pearson entre indicadores"))
    st.dataframe(matriz)
    r=matriz.loc["area_desmatada_km2","focos_queimada"]
    st.write(f"Foram analisados {len(df)} registros. " + (f"Pearson entre queimadas e desmatamento: {numero(r,4)}. Valores próximos de zero indicam pouca associação linear neste recorte; o coeficiente varia de −1 a +1." if pd.notna(r) else "Correlação indefinida: faltam observações ou variação nas variáveis do recorte."))
    st.warning("Correlação não demonstra causalidade. Observações mensais e geográficas podem ser dependentes; esta é uma análise descritiva, sem inferência causal ou teste de significância.")
    st.subheader("Conclusão executiva")
    st.write("Use o coeficiente e a dispersão em conjunto. Mesmo um coeficiente pequeno não exclui relações não lineares; a geração simulada e a composição do recorte limitam a interpretação ambiental.")

def explorar():
    cabecalho("Exploração detalhada e transparência do tratamento da base.")
    st.subheader("Qualidade e preparação")
    st.json(qualidade)
    st.write("Datas convertidas, categorias normalizadas, números validados, duplicatas exatas removidas e datas conferidas com ano e mês. Linhas inválidas são excluídas e contabilizadas, sem inventar valores. Atributos derivados: trimestre, período mensal e indicador de risco elevado.")
    st.warning("A base apresenta combinações de UF e bioma que podem não representar a geografia real. Foram preservadas como fornecidas na simulação; nenhum mapa geográfico é usado para validar essas combinações.")
    st.subheader("Tabela dinâmica")
    grupo=st.selectbox("Agrupar por",["uf","bioma","regiao","ano","nivel_risco"])
    tabela=df.groupby(grupo,as_index=False).agg(registros=("ano","size"),area_desmatada_km2=("area_desmatada_km2","sum"),area_preservada_media_km2=("area_preservada_km2","mean"),focos_queimada=("focos_queimada","sum"),emissoes_co2=("emissoes_co2","sum"))
    st.dataframe(tabela,hide_index=True,width="stretch")
    st.subheader("Registros filtrados")
    st.dataframe(df,hide_index=True,width="stretch")
    st.subheader("Conclusão executiva")
    st.write("O tratamento permite reproduzir os indicadores sem alterar o CSV original. A cobertura de 20 UFs e as limitações da simulação devem acompanhar qualquer apresentação dos resultados.")

pagina=st.navigation([st.Page(resumo,title="Visão geral",default=True),st.Page(temporal,title="Evolução temporal"),st.Page(correlacoes,title="Correlação ambiental"),st.Page(explorar,title="Exploração dos dados")])
pagina.run()
