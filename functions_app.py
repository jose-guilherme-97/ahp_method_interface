import streamlit as st
import pandas as pd

# Classe que apoia a montagem de dataframes e outras operações correlatas para compor
# os objetos necessários para execução do programa
class DealWithDf:
    def __init__(self) -> None:
        pass

    def replace_matching_indices_with_1(self, df):
        """
        Função que garante diagonal principal de uma matriz com valor 1

        Args:
            df (dataframe pandas): dataframe cujos valores compõe uma matriz quadrada
        
        Returns:
            df (dataframe pandas)
        """
        # Iterando sobre o dataframe
        for idx in df.index:
            for col in df.columns:
                # Checando se o index é o mesmo que a coluna
                if idx == col:
                    # garantindo a diagonal princial igual a 1
                    df.loc[idx, col] = 1
        return df

    def create_dataframe_from_list(self, list_of_strings):
        """
        Função que cria um dataframe tendo como índices e colunas uma mesma lista de strings

        Args:
            list_of_strings (list): lista de strings
        
        Returns:
            df (dataframe pandas): dataframe contendo como index e colunas a lista recebida
        """
        # Criando um dataframe baseado em lista de índices (cria uma matriz quadrada com índices e colunas)
        df = pd.DataFrame(index=list_of_strings, columns=list_of_strings)
        df = df.fillna("-")
        df = self.replace_matching_indices_with_1(df)
        return df

    def create_judgement_table(self, df, type):
        """
        Função que cria um dataframe tendo como valores a matriz de julgamento

        Args:
            df (dataframe pandas): dataframe que contém os critérios como índices e colunas
            type (str): valor que ajuda a criar objetos de entradas no streamlit com diferentes IDs
        
        Returns:
            df (dataframe pandas): dataframe contendo os valores da matrix de julgamento fornecidos pelo
            usuário
        """
        index = list(df.index)
        columns = list(df.columns)
        for i in range(len(index)):
            for j in range(i + 1, len(columns)):
                cell_value = st.selectbox(f"Qual a relação de importância entre {index[i]} e {columns[j]}", 
                                        ("1/9", "1/8","1/7","1/6","1/5","1/4","1/3","1/2","1","2","3","4",
                                        "5","6","7","8","9"),
                                        key=f"{type}_{i}_{j}")
                if "/" in cell_value:
                    numbers = cell_value.split("/")
                    cell_value = int(numbers[0]) / int(numbers[1])

                df.at[index[i], columns[j]] = float(cell_value)
                df.at[columns[j], index[i]] = 1 / float(cell_value)    
        return df

    def create_decision_table(self, data_alternativas, data_criterios, flag, dict_quali = None):
        """
        Função que cria um dataframe tendo como valores a matriz de decisão fornecida pelo usuário

        Args:
            data_alternativas (dataframe pandas): df contendo as alternativas fornecidas
            data_criterios (dataframe pandas): df contendo os critérios fornecidos
            flag (bool): variável que indica se há presença de critérios qualitativos
            dict_quali (dict): dicionário que contém o de / para entre valores qualitativos e seus respectivos
            pesos calculados
        
        Returns:
            df (dataframe pandas): dataframe contendo como valor a matriz de decisão
        """
        if flag == True and dict_quali == None:
            raise ValueError("Quando flag é True (indicando que houve critérios qualitativos), dict_quali não pode ser None")
        
        index = list(data_alternativas["alternativas"])
        columns = list(data_criterios["criterios"])
        decision_matrix = pd.DataFrame(index = index, columns = columns)

        for i in range(len(index)):
            for j in range(len(columns)):
                tipo = data_criterios[data_criterios["criterios"] == columns[j]]["tipo"].values[0]
                if tipo == "quantitativo":
                    cell_value = st.number_input(f"Indique o valor quando a alternativa for {index[i]} e o critério {columns[j]}", key = f"{i}_{j}")
                if tipo == "qualitativo":
                    valores_possiveis = tuple(dict_quali[columns[j]].keys())
                    aux_value = st.selectbox(f"Indique o valor quando a alternativa for {index[i]} e o critério {columns[j]}"
                                            ,valores_possiveis
                                            , key = f"{i}_{j}")
                    cell_value = dict_quali[columns[j]][aux_value]
                decision_matrix.at[index[i], columns[j]] = cell_value
        return decision_matrix

    def color_coding(self, row, max, min):
        """
        Função que cria um mapeamento em um dataframe para definição de cores personalizadas baseando-se
        em uma coluna de resultados.

        Args:
            row (tuple): linha do dataframe percorrido
            max (float): valor máximo presente na coluna 'resultados'
            min(float): valor mínimo presente na coluna 'resultados'
        
        Returns:
            result (list): Lista contendo o mapeamento de cores a ser aplicado
        """
        if row.resultados == max:
            result = ['background-color:green'] * len(row) 
        elif row.resultados != min: 
            result = ['background-color:yellow'] * len(row) 
        else:
            result = ['background-color:red'] * len(row)
        return result