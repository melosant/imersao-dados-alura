# Imersão Dados com Python : Alura
# Aula 1: Explore Dados com Pandas
import pandas as pd

# ----- Importação DF -------
df = pd.read_csv('https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv')
print(df.head())


# ----- Primeiras Informações DF -----
print('\nPrimeiras Informações\n')
print(df.info()) # informações colunas 
print(df.describe()) # informações numéricas
print(df.shape) # tamanho do df (0 - linhas, 1 - colunas)
print(df.columns) # nome das colunas


# ----- Renomeando Colunas ------
print('\nRenomeando Colunas\n')
map_colunas = {
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda',
    'salary_in_usd': 'usd',
    'employee_residence': 'residencia', 
    'remote_ratio': 'remoto',
    'company_location': 'localizacao_empresa',
    'company_size': 'tamanho_empresa'
} 
df.rename(columns=map_colunas, inplace=True)
print(df.head())


# ----- Visualização qtd de valores -----
print('\nView Qtd de Valores\n')
print(df['senioridade'].value_counts())
print(df['contrato'].value_counts())
print(df['remoto'].value_counts())
print(df['tamanho_empresa'].value_counts())


# ----- renomeando valores (categorias) ------
print('\nRenomeando Valores\n')
map_senior = {
    'SE': 'Sênior',
    'MI': 'Pleno',
    'EN': 'Júnior',  
    'EX': 'Executivo'
}
df['senioridade'] = df['senioridade'].replace(map_senior)
print(df['senioridade'].value_counts())

map_contrato = {
    'FT': 'Integral',
    'CT': 'Contrato',
    'PT': 'Meio-Período',
    'FL': 'Freelancer'
}
df['contrato'] = df['contrato'].replace(map_contrato)
print(df['contrato'].value_counts())

map_remoto = {
    '0': 'Presencial',      
    '100': 'Remoto',     
    '50': 'Meio-Período'        
}
df['remoto'] = df['remoto'].replace(map_remoto)
print(df['remoto'].value_counts())

map_tamanho = {
    'M': 'Médio',   
    'L': 'Grande',     
    'S': 'Pequeno'      
}
df['tamanho_empresa'] = df['tamanho_empresa'].replace(map_tamanho)
print(df['tamanho_empresa'].value_counts())


# ----- describe objects -----
print('\nDescrição Não Numérica\n')
print(df.describe(include='object'))


# ----- resultado ------
print('\nResultado\n')
print(df.head())