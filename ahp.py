import numpy as np
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO")

# Classe utilizada para operações com a matriz de jugamento (do processo ou de um critério)
class MatrizJulgamento:
    def __init__(self) -> None:
        logging.info("Iniciando a classe da matriz de julgamento")
        

    def checa_reciprocidade(self, matriz):
        """
        Função que verifica o princípio da reciprocidade da matriz: aij = aji

        Args:
            matriz (numpy array): matriz de julgamento
        
        Returns:
            message (str): texto indicando o veredito do processo
            status (int): código indicando o status do processo
        """
        logging.info("Checando o princípio da reciprocidade para a matriz de julgamento")
        shape = matriz.shape
        linhas = shape[0]
        colunas = shape[1]
        
        if linhas != colunas:
            message = "A matriz não é quadrada"
            status = 400
            return message, status
        
        for i in range(linhas):
            for j in range(i+1, colunas):
                if matriz[i][j] != 1./matriz[j][i]:
                    message = f"Falha na reciprocidade: o elemento a{i}{j} deve ser igual a 1/a{j}{i}"
                    status = 400
                    return message, status
        return "OK", 200

    def verifica_qualidade_matriz(self, matriz):
        """
        Função que verifica a consistência da diagonal principal (deve ser composta apenas por '1')

        Args:
            matriz (numpy array): matriz de julgamento
        
        Returns:
            message (str): texto indicando o veredito do processo
            status (int): código indicando o status do processo
        """
        logging.info("Checando a consistência da diagonal principal da matriz de julgamento")
        diag = np.unique(np.diagonal(matriz))
        if len(diag) != 1:
            message = "A diagonal da matriz de julgamento deve ser composta apenas pelo elemento 1"
            status = 400
            return message, status
        
        if diag[0] != 1:
            message = f"A diagonal da matriz de julgamento deve ser composta apenas pelo elemento 1"
            status = 400
            return message, status
        return "OK", 200
    
    def normalizacao_julgamentos(self, matriz):
        """
        Função que calcula o vetor prioridade da matriz de julgamento. Este vetor busca traduzir
        em termos percentuais o grau de importância de cada critério ou qualidade

        Args:
            matriz (numpy array): matriz de julgamento
        
        Returns:
            vetor_prioridade (numpy array): vetor prioridade com percentuais de importância de cada critério
        """
        logging.info("Retornando o vetor prioridade da matriz de julgamento")
        soma_linhas = np.sum(matriz, axis = 0, dtype='f')
        matriz_normalizada = matriz / soma_linhas
        vetor_prioridade = np.mean(matriz_normalizada, axis = 1, dtype='f').reshape((-1,1))
        return vetor_prioridade
    
    def analise_consistencia(self, matriz, vetor_prioridade):
        """
        Função que realiza o teste de constência proposto por Thomas Saaty. O processo visa calcular
        a razão entre o índice de consistência (gerado a partir da aplicação dos pesos do vetor
        prioridade sobre cada coluna correspondente (critério)) e o índice aleatório (tabelado, com
        valores também propostos e fixos a depender da quantidade de critérios).

        Args:
            matriz (numpy array): matriz de julgamento
            vetor_prioridade (numpy array): vetor prioridade
        
        Returns:
            cr (float): raio de consistência. Valor que indica o quão coerente foi o processo de 
            atribuição de pesos da matriz de julgamento
        """
        logging.info("Checando a consistência dos graus de importância atribuídos na matriz de julgamento")
        random_index = [0, 0 , 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.48, 1.56, 1.57, 1.59]
        tamanho = vetor_prioridade.shape[0]
        matriz_auxiliar = matriz
        for i in range(tamanho):
            matriz_auxiliar[:, i] = matriz_auxiliar[:, i] * vetor_prioridade[i][0]

        soma_pesos = np.sum(matriz_auxiliar, axis = 1, dtype='f').reshape((-1,1))
        vetor_lambda = soma_pesos / vetor_prioridade
        lambda_max = np.sum(vetor_lambda, dtype='f') / tamanho
        ci = (lambda_max - tamanho) / (tamanho - 1)
        cr = ci / random_index[tamanho - 1]
        cr = cr * 100
        return cr
        
class MatrizDecisao:
    def __init__(self) -> None:
        logging.info("Iniciando a classe da matriz de decisão")

    def normalizacao_decisao(self, matriz_decisao, lista_referencia_monotomica):
        """
        Função que normaliza os valores da matriz de decisão (converte-os para uma mesma unidade
        comparável, em percentuais)

        Args:
            matriz (numpy array): matriz de julgamento
            lista_referencia_monotomica (list): lista contendo '-1' (critério monotômico de custo) ou
            '1' (critério monotômico de lucro)
        
        Returns:
            matriz_normalizada (numpy array): matriz normalizada com as adequações necessárias
        """
        logging.info("Normalizando os valores da matriz de decisão (descrição em percentuais)")
        matriz_auxiliar = matriz_decisao
        for i in range(len(lista_referencia_monotomica)):
            if lista_referencia_monotomica[i] == -1:
                matriz_auxiliar[:, i] =  1.0 / matriz_auxiliar[:, i]
        
        soma_linhas = np.sum(matriz_auxiliar, axis = 0, dtype='f')
        matriz_normalizada = matriz_auxiliar / soma_linhas
        return matriz_normalizada

class AHP:
    def __init__(self, matriz_julgamento, matriz_decisao, lista_referencia_monotomica) -> None:
        logging.info("Iniciando a classe AHP")
        self.matriz_julgamento = matriz_julgamento
        self.matriz_decisao = matriz_decisao
        self.lista_referencia_monotomica = lista_referencia_monotomica
    
    def executa_algoritmo(self):
        """
        Função que executa o algoritmo e coordena os passos lógicos de sua execução

        Args:
            None
        
        Returns:
            resultado (numpy array): vetor que indica, para cada alternativa, o qual sua relevância (ordem)
            no processo de tomada de decisão
        """
        logging.info("Executando o algoritmo")
        class_matriz_julgamento = MatrizJulgamento()
        class_matriz_decisao = MatrizDecisao()
        message, status = class_matriz_julgamento.verifica_qualidade_matriz(self.matriz_julgamento)
        if status != 200:
            raise ValueError(message)
        
        message, status = class_matriz_julgamento.checa_reciprocidade(self.matriz_julgamento)
        if status != 200:
            raise ValueError(message)
        
        vetor_prioridade = class_matriz_julgamento.normalizacao_julgamentos(self.matriz_julgamento)
        consistencia = class_matriz_julgamento.analise_consistencia(self.matriz_julgamento, vetor_prioridade)
        if consistencia > 10:
            message = f"""O teste de consistência da matriz de julgamento reprovou as prioridades definidas.\n
                        O resultando da razão de consistência deve ser menor que 10%. O valor encontrado foi
                        {consistencia}"""
            raise ValueError(message)
        
        matriz_normalizada = class_matriz_decisao.normalizacao_decisao(self.matriz_decisao, self.lista_referencia_monotomica)
        resultado = np.dot(matriz_normalizada, vetor_prioridade)
        return resultado
