import pandas as pd
import numpy as np
import io
import zipfile
import requests # Usado para baixar os dados


# --- 1. Definição de Variáveis e Layout ---
# https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/Documentacao/Dicionario_e_input_20221031.zip
# Arquivo: dicionario_PNADC_microdados_trimestral.xls
#
# Extraídas do Dicionário de Variáveis
# da PNAD ContínGua para o trimestre/ano específico.
#
# Variáveis de interesse para a nossa pergunta de pesquisa:
# V2007: Sexo
# V2010: Cor ou raça
# VD3004: Nível de instrução mais elevado alcançado
# VD4002: Condição de ocupação na semana de referência
# VD4009 - Posicao_Ocupacao 
# V1028: Peso amostral (essencial para qualquer análise do IPEA)

# (colspecs) é uma lista de tuplas (início, fim) da posição de cada variável (-1 da posição devido o ínio do índice em python)
colspecs = [
    (94, 95),   # V2007 - Sexo
    (106, 107), # V2010 - Cor ou raça
    (404, 405), # VD3004 - Nível de instrução
    (416, 418), # VD4009 - Posicao_Ocupacao        
    (49, 65),   # V1028 - Peso amostral
]

names = [
    'V2007_Sexo',
    'V2010_Cor_Raca',
    'VD3004_Nivel_Instrucao',
    'VD4009_Posicao_Ocupacao',
    'V1028_Peso'
]


print("Iniciando a leitura dos microdados...")
fileExtract = "PNADC_032025.txt"

data_file_name = fileExtract


# --- 2. Leitura dos Microdados ---
# https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/2025/PNADC_032025.zip
# Arquivo PNADC_032025.txt

try:
    df = pd.read_fwf(
        data_file_name,
        colspecs=colspecs,       # Define as posições das colunas
        names=names,             # Nomeia as colunas
        dtype=str                # Importa tudo como string para consistência
    )
    #print(f"Sucesso: {len(df)} registros importados.")
    #print("\n 1) V1028_Peso: ", df['V1028_Peso'].unique())
    #print("\n 2) V2007_Sexo:", df['V2007_Sexo'].unique())
    #print("\n 3) V2010_Cor_Raca: ", df['V2010_Cor_Raca'].unique())
    #print("\n 4) VD3004_Nivel_Instrucao: ", df['VD3004_Nivel_Instrucao'].unique())
    #print("\n 5) VD4009_Posicao_Ocupacao: ", df['VD4009_Posicao_Ocupacao'].unique())


except FileNotFoundError:
    print(f"ERRO: O arquivo '{data_file_name}' não foi encontrado.")
    print("Este é um script de demonstração. Um DataFrame vazio será criado.")
    df = pd.DataFrame(columns=names) # Cria um DF vazio para o script continuar

except Exception as e:
    print(f"Ocorreu um erro inesperado durante a leitura: {e}")
    df = pd.DataFrame(columns=names)

# --- 3. Padronização de Variáveis  ---
# Transformar alguns dados numéricos em categóricos

if not df.empty:
    # 3.1. Limpeza de 'NA' (Valores não aplicáveis ou missing)
    # A PNAD usa ' ' ou '9's. Vamos tratar como string.
    
    # 3.2. Recodificação de Variáveis
    
    # Sexo (V2007)
    df['SEXO'] = df['V2007_Sexo'].map({
        '1': 'Homem',
        '2': 'Mulher'
    })
    
    # Cor/Raça (V2010) - Agrupando em Brancos e Não-Brancos (Pretos/Pardos)
    df['RACA_COR'] = df['V2010_Cor_Raca'].map({
        '1': 'Branca',
        '2': 'Preta',
        '3': 'Amarela',
        '4': 'Parda',
        '5': 'Indígena',
        '9': 'Ignorado'
    })
    
    # Nível de Instrução (VD3004) - Agrupando para nossa pergunta
    # Vamos criar a variável "Ensino Médio Completo ou mais"
    niveis_ensino_medio_mais = ['5', '6', '7'] # Médio completo, Superior incompleto, Superior completo
    df['EDUCA'] = df['VD3004_Nivel_Instrucao'].apply(
        lambda x: 'Médio completo ou mais' if x in niveis_ensino_medio_mais else 'Médio incompleto ou menos'
    )
    
    # Ocupação Formal (VD4009) - Nossa variável dependente
    # 01 = Empregado com carteira (Formal)
    # 02 = Empregado sem carteira (Informal)
    # 03 = Trabalhador doméstico com carteira (Formal)
    # 04 = Trabalhador doméstico sem carteira (Informal)
    # 05 = Militar/Servidor Estatutário (Formal)
    # 06 = Conta própria (Geralmente Informal, a menos que pague INSS - vamos simplificar como Informal para este teste ou usar VD4012)
    # 07 = Empregador (Formal)
    # ...

    # Regra ocupação
    def definir_formalidade(codigo):
        formais = ['01', '03', '05', '07'] # Com carteira, militares, estatutários, empregadores
        informais = ['02', '04', '06', '08', '09', '10'] # Sem carteira, conta própria, familiar auxiliar
    
        if codigo in formais:
            return 'Ocupado Formal'
        elif codigo in informais:
            return 'Ocupado Informal'
        else:
            return 'Desocupado/Fora' # Para códigos nulos ou fora da força de trabalho

    df['TRABALHO'] = df['VD4009_Posicao_Ocupacao'].apply(definir_formalidade)

    # 3.3. Conversão do Peso
    df['PESO'] = pd.to_numeric(df['V1028_Peso'], errors='coerce')
    
    # 3.4. Seleção final de colunas limpas
    df_limpo = df[['SEXO', 'RACA_COR', 'EDUCA', 'TRABALHO', 'PESO']].dropna()
    
    #print("\n--- DF Limpo ---")
    #print(df_limpo.head(500))
    
    #print("\n--- Amostra do DataFrame Padronizado ---")
    #numero_de_linhas = len(df_limpo)
    #print(f"O número total de linhas é: {numero_de_linhas}")
    
    # (Presume-se que 'df_limpo' existe do script anterior)
    # 'df_limpo' contém as colunas: ['SEXO', 'RACA_COR', 'EDUCA', 'TRABALHO', 'PESO']
    print("\n--- 4. Geração de Indicadores (Item iii) ---")

    # 4.1. Refinamento da Amostra e Variáveis para Análise
    # Para a "Taxa de Formalidade", analisamos apenas a População Ocupada.
    df_ocupado = df_limpo[
        df_limpo['TRABALHO'].isin(['Ocupado Formal', 'Ocupado Informal'])
    ].copy()

    # A Disoc/IPEA frequentemente agrupa 'Preta' e 'Parda' em 'Negra'.
    # Vamos padronizar isso.
    df_ocupado['RACA_GRUPO'] = df_ocupado['RACA_COR'].map({
        'Branca': 'Branca',
        'Preta': 'Preta/Parda',
        'Parda': 'Preta/Parda'
    })

    # Removemos da análise os grupos não focais (Amarela, Indígena, Ignorado)
    df_ocupado = df_ocupado.dropna(subset=['RACA_GRUPO'])

    # Criar a variável binária (target) para o cálculo da taxa
    # 1 se for Formal, 0 se for Informal
    df_ocupado['É_FORMAL'] = (df_ocupado['TRABALHO'] == 'Ocupado Formal').astype(int)


    # 4.2. Definição da Função de Média Ponderada
    # A forma de calcular taxas com microdados de surveys (PNAD, PME)
    # é usando os pesos amostrais (V1028_Peso).
    def media_ponderada(grupo, col_valor, col_peso):
        """
        Calcula a média ponderada para um grupo do DataFrame.
        (Soma de (Valor * Peso)) / (Soma dos Pesos)
        """
        d = grupo[col_valor]
        w = grupo[col_peso]
        try:
            return (d * w).sum() / w.sum()
        except ZeroDivisionError:
            return np.nan

    # 4.3. Agrupamento e Cálculo dos Indicadores
    # Estes são os grupos definidos na pergunta de pesquisa
    grupos_analise = ['EDUCA', 'SEXO', 'RACA_GRUPO']

    indicadores = df_ocupado.groupby(grupos_analise).apply(media_ponderada, 'É_FORMAL', 'PESO', include_groups=False)

    # Aplicar a função ponderada para calcular a taxa de formalidade
    tabela_resultados = (indicadores * 100).round(1).unstack('RACA_GRUPO')

    # Reordenar colunas para melhor leitura
    tabela_resultados = tabela_resultados[['Branca', 'Preta/Parda']]

    # Renomear os índices
    tabela_resultados.index.names = ['Nível de Instrução', 'Sexo']

    print("\n--- Resultados - Tabela de Indicadores ---")
    print("Taxa de Formalidade da População Ocupada (%) por Instrução, Sexo e Raça/Cor")
    print(tabela_resultados)
    
    
else:
    print("DataFrame está vazio. A padronização foi pulada.")
