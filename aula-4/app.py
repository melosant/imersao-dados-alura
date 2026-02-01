import pandas as pd
import streamlit as st
import plotly.express as px

# config pagina
st.set_page_config(
    page_title='Dashboard de Salários na Área de Dados',
    layout='wide'
)

df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# sidebar de filtros
st.sidebar.header('Filtros')
anos_disponiveis = sorted(df['ano'].unique())
anos_select = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis)
senioridade_disponiveis = sorted(df['senioridade'].unique())
senioridade_select = st.sidebar.multiselect('Senioridade', senioridade_disponiveis, default=senioridade_disponiveis)
contrato_disponiveis = sorted(df['contrato'].unique())
contrato_select = st.sidebar.multiselect('Tipo de Contrato', contrato_disponiveis, default=contrato_disponiveis)
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_select = st.sidebar.multiselect('Tamanho da Empresa', tamanhos_disponiveis, default=tamanhos_disponiveis)

df_filtrado = df[
    (df['ano'].isin(anos_select)) &
    (df['senioridade'].isin(senioridade_select)) &
    (df['contrato']).isin(contrato_select) &
    (df['tamanho_empresa'].isin(tamanhos_select))
]

# main da pagina
st.title('Dashboard de Análise de Salários na Área de Dados')
st.markdown('Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.')

# exibe métricas gerais
st.subheader('Métricas gerais (Salário Anual em USD)')
if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_max = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio, salario_max, total_registros, cargo_mais_frequente = 0, 0, 0, ''
col1, col2, col3, col4 = st.columns(4)
col1.metric('Salário Médio', f'${salario_medio:,.0f}')
col2.metric('Salário Máximo', f'${salario_max:,.0f}')
col3.metric('Total de Registros', f'{total_registros:,}')
col4.metric('Cargo mais frequente', cargo_mais_frequente)

st.markdown('---')
st.subheader('Gráficos')
col_graf1, col_graf2 = st.columns(2)
# gráfico barra de 10 cargos com maior salario
with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            data_frame=top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title='Top 10 cargos por salário médio',
            labels={'usd': 'Média Salarial Anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de cargos.')

# grafico histograma de distribuição salarial
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title='Distribuição de Salários Anuais',
            labels={'usd': 'Faixa Salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de distribuição.')

col_graf3, col_graf4 = st.columns(2)

# grafico pie para proporção de tipos de trabalho
with col_graf3:
    if not df_filtrado.empty:
        remoto_count = df_filtrado['remoto'].value_counts().reset_index()
        remoto_count.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_count,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

# '''
# PARA O CÓDIGO POR PAÍSES ESTAR EM ISO 3

# def iso2_to_iso3():
#     try:
#         return pycountry.countries.get(alpha_2=code).alpha_3
#     except:
#         return None

# df_limpo['residencia_iso3] = df_limpo['residencia].apply(iso2_to_iso3)
# '''

# grafico maior media salarial de Cientista por país (mostra no mapa)
with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        mean_country = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(mean_country,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 

st.markdown('---')
st.subheader('Dataframe Filtrado')
st.dataframe(df_filtrado)