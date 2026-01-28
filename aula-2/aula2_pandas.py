# Aula 1 - Pandas Comandos Básicos
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv')
renomear_colunas = {
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda',
    'salary_in_usd': 'usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remoto',
    'company_location': 'empresa',
    'company_size': 'tamanho_empresa'
}
df.rename(columns=renomear_colunas, inplace=True)
senioridade = {
    'SE': 'Sênior',
    'MI': 'Pleno',
    'EN': 'Júnior',
    'EX': 'Executivo'
}
df['senioridade'] = df['senioridade'].replace(senioridade)
tipo_trabalho = {
    'FT': 'Integral',
    'PT': 'Meio-Período',
    'CT': 'Contrato',
    'FL': 'Freelancer'
}
df['contrato'] = df['contrato'].replace(tipo_trabalho)
mapa_remoto = {
    0: 'Presencial',
    50: 'Híbrido',
    100: 'Remoto'
}
df['remoto'] = df['remoto'].replace(mapa_remoto)
mapa_tamanho = {
    'S': 'Pequeno',
    'M': 'Médio',
    'L': 'Grande'
}
df['tamanho_empresa'] = df['tamanho_empresa'].replace(mapa_tamanho)

# ----------------------------------------------------------------------------

# AULA 2: TRATAMENTO DE DADOS

# ----- conferência dos nulos, e valores únicos de uma coluna -----
print(df.isnull())
print(df.isnull().sum())
print(df['ano'].unique())
print(df[df.isnull().any(axis=1)])

import numpy as np

# criação de um df para exemplo
df_salarios = pd.DataFrame({
    'nome': ['João', 'Maria', 'José', 'Ana', 'Val'],
    'salario': [4000, np.nan, 5000, np.nan, 100000]
})
# substitui os nulls pela media
df_salarios['salario_media']= df_salarios['salario'].fillna(df_salarios['salario'].mean().round(2))
# substitui os nulls pela mediana
df_salarios['salario_mediana'] = df_salarios['salario'].fillna(df_salarios['salario'].median())
print(df_salarios)

df_temperaturas = pd.DataFrame({
    'DiaSemana': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'],
    'Temperatura': [30, np.nan, np.nan, 28, 27]
})
# completa com o valor anterior
df_temperaturas['preenchido_ffill'] = df_temperaturas['Temperatura'].ffill()
# completa com o valor posterior
df_temperaturas['preenchido_bfill'] = df_temperaturas['Temperatura'].bfill()
print(df_temperaturas)

df_cidades = pd.DataFrame({
    'nome': ['João', 'Maria', 'José', 'Ana', 'Val'],
    'cidades': ['São Paulo', np.nan, 'Belo Horizonte', np.nan, 'Rio de Janeiro']
})

# preenche os nulls com o valor informado
df_cidades['fill_cidades'] = df_cidades['cidades'].fillna('Não Informado')
print(df_cidades)

# dropa os nulls
df_limpo = df.dropna()
df_limpo.isnull().sum()
print(df_limpo.head())

# converte o tipo de ano (float -> int)
df_limpo = df_limpo.assign(ano = df_limpo['ano'].astype('int64'))
df_limpo.info()