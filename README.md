# Análise de Microdados (PNAD Contínua)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## 1. Contexto do Projeto
O objetivo é demonstrar de forma prática como manipular dados do PNAD.
* Conhecimento em **Python** para análise de dados.
* Capacidade de responder a uma pergunta de pesquisa nas áreas sociais - no caso, a área selecionada foi a de Educação.
* Demonstração da metodologia, análise e reprodutibilidade do código.

## 2. 🎯 Objetivo da Análise
A pergunta de pesquisa central que este projeto responde é:

> "Qual é a associação entre o nível de instrução (possuir Ensino Médio completo ou mais) e a taxa de formalidade no mercado de trabalho, e como essa associação difere entre os grupos de gênero (homens e mulheres) e raça/cor (brancos e pretos/pardos) na população ocupada brasileira?"

## 3. 📊 Fonte de Dados
A análise utiliza os microdados públicos da **Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua)**, disponibilizados pelo IBGE.

* **Microdados:** [PNADC_032025.zip (3º Trimestre 2025)](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/2025/PNADC_032025.zip)
* **Dicionário de Variáveis:** [Dicionario_e_input_...zip](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/Documentacao/Dicionario_e_input_20221031.zip)

## 4. 📈 Resultados Principais
O script em Python (`IBGE_Microdados_PNAD_2025.py`) processa os microdados brutos, aplica os pesos amostrais (`V1028`) e gera a seguinte tabela de indicadores.

**Tabela 1:** Taxa de Formalidade da População Ocupada (%) por Nível de Instrução, Sexo e Raça/Cor. Brasil, 3º Trim. 2025

| Nível de Instrução | Sexo | Raça/Grupo (Taxa de Formalidade em %) | |
| :--- | :--- | :---: | :---: |
| | | **Branca** | **Preta/Parda** |
| **Médio completo ou mais** | Homem | 54,4% | 57,2% |
| | Mulher | 58,0% | 55,4% |
| **Médio incompleto ou menos** | Homem | 34,9% | 32,1% |
| | Mulher | 35,7% | 31,1% |

*Fonte: Elaboração própria a partir dos microdados da PNAD Contínua (IBGE, 2025).*

## 5. 🚀 Como Reproduzir a Análise
Este projeto foi desenvolvido visando a **reprodutibilidade**.

### Requisitos
* Python 3.x
* Pandas
* Numpy

(Recomenda-se criar um ambiente virtual e instalar via `pip install pandas numpy`)

### Passos para Execução

1.  **Clone o repositório:**
    ```bash
    git clone [URL-DO-SEU-REPOSITORIO-AQUI]
    cd [NOME-DO-SEU-REPOSITORIO]
    ```

2.  **Baixe os Dados:**
    * Faça o download dos microdados (link acima).
    * Descompacte o arquivo `PNADC_032025.zip`.
    * Coloque o arquivo `PNADC_032025.txt` dentro da pasta do repositório.

3.  **Execute o Script:**
    ```bash
    python analise_pnad.py
    ```
    (O script irá imprimir no terminal os resultados da Tabela 1.)

## 6. 📄 Licença
Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.
