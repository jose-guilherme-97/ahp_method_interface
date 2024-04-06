import streamlit as st
import pandas as pd
import uuid
import ahp
from functions_app import DealWithDf

# Inicializando algumas listas para coletar alternativas e critérios
rows_collection_alt = []
rows_collection_cri = []

# Inicializando alguns estatos utilizados no processo de 
if "alternativas" not in st.session_state:
    st.session_state["alternativas"] = []

if "criterios" not in st.session_state:
    st.session_state["criterios"] = []

if 'alternativas_concluidas' not in st.session_state:
    st.session_state.alternativas_concluidas = False

if 'criterios_concluidos' not in st.session_state:
    st.session_state.criterios_concluidos = False

if f"criterio_quali_concluido" not in st.session_state:
    st.session_state[f"criterio_quali_concluido"] = False

if f"criterios_quali_finalizados_por_completo" not in st.session_state:
    st.session_state[f"criterios_quali_finalizados_por_completo"] = False

if f"matriz_julgamento" not in st.session_state:
    st.session_state["matriz_julgamento"] = False

if f"matriz_decisao" not in st.session_state:
    st.session_state["matriz_decisao"] = False

# Concentrando a classe que coordena o acionamento de botões
class Button:
    def __init__(self) -> None:
        pass

    def click_button_alternativas_concluidas(self):
        st.session_state.alternativas_concluidas = True

    def click_button_criterios_concluidos(self):
        st.session_state.criterios_concluidos = True

    def click_button_criterio_quali_concluido(self, id):
        st.session_state[id] = True
    
    def click_button_consistencia_quali(self, id):
        st.session_state[id] = True

    def click_button_criterios_quali_fim(self):
        st.session_state["criterios_quali_finalizados_por_completo"] = True

    def click_button_matriz_julgamento(self):
        st.session_state["matriz_julgamento"] = True

    def click_button_matriz_decisao(self):
        st.session_state["matriz_decisao"] = True

# Classe que coordena o processo de inserção de dados pelo tomador de decisão
class CollectInfos:
    def __init__(self) -> None:
        pass

    def add_row(self, type):
        """
        Função que adiciona uma linha para que o usuário possa informar mais um valor

        Args:
            type (str): indica a etapa ao qual deseja-se inserir linhas (alternativas, critérios, etc.)
        
        Return:
            None
        """
        element_id = uuid.uuid4()
        st.session_state[type].append(str(element_id))

    def remove_row(self, row_id, type):
        """
        Função que remove uma linha

        Args:
            row_id (str, int): indica o id utilizado para a linha que deseja-se excluir
            type (str): indica a etapa ao qual deseja-se inserir linhas (alternativas, critérios, etc.)
        
        Return:
            None
        """
        st.session_state[type].remove(str(row_id))

    def generate_row(self, row_id, type):
        """
        Função que coordena a aparição/exclusão de uma linha e capta a informação fornecida pelo usuário

        Args:
            row_id (str, int): indica o id utilizado para a linha trabalhada
            type (str): indica a etapa ao qual deseja-se inserir linhas (alternativas, critérios, etc.)
        
        Return:
            (dict): dicionário contendo as informações coletadas
        """
        if type == "alternativas":
            row_container = st.empty()
            row_columns = row_container.columns((3,1))
            row_name = row_columns[0].text_input("Alternativa", key=f"txt_{row_id}")
            row_columns[1].button("🗑️", key=f"del_{row_id}", on_click=self.remove_row, args=[row_id, type])
            return {"name": row_name}
        
        if type == "criterios":
            row_container = st.empty()
            row_columns = row_container.columns((3, 2, 3, 1))
            row_name = row_columns[0].text_input("Criterios", key=f"txt_{row_id}")
            row_type = row_columns[1].selectbox("Tipo", ("quantitativo", "qualitativo"), key=f"tipo_{row_id}")
            row_charac = row_columns[2].selectbox("Característica", ("Quanto maior, melhor", "Quanto maior, pior", "Não Aplicável"), key=f"carac_{row_id}")
            row_columns[3].button("🗑️", key=f"del_{row_id}", on_click=self.remove_row, args=[row_id, type])
            return {"name": row_name, "tipo": row_type, "caracteristica": row_charac}

        if "criterios_quali" in type:
            row_container = st.empty()
            row_columns = row_container.columns((3,1))
            row_name = row_columns[0].text_input("Valores Qualitativos", key=f"txt_{row_id}")
            row_columns[1].button("🗑️", key=f"del_{row_id}", on_click=self.remove_row, args=[row_id, type])
            return {"name": row_name}

# Inicialização das classes importantes a serem utilizadas
botoes = Button()
coordena_coleta = CollectInfos()
df_opps = DealWithDf()

# Construção da visualização inicial do usuário. Uma tela informando o propósito, modelo, origem, criador e
# qual a lógica de construção e limitações do algoritmo
with st.container():
    st.title("Modelo de apoio à tomada de decisão multicritérios")
    st.subheader("O método AHP (Analytic Hierarchy Process)")
    menu = st.columns([3,1])
    with menu[0]:
        texto1 = """Desenvolvido na década de 1970 pelo professor [Thomas Saaty](https://pt.wikipedia.org/wiki/Thomas_Saaty),
             o modelo busca fundamentar escolhas através de uma abordagem científica, tornando possível quantificar e ordenar
             escolhas baseadas em um conjunto de alternativas possíveis (soluções) e critérios estabelecidos. Com isso,
             o(s) tomador(es) de decisão pode(m), a partir da definição de priorizações e importância entre critérios,
             direcionar qual a melhor decisão baseando-se nos mesmos."""
        st.write(f'{texto1}')
    with menu[1]:
        st.image("Saaty.jpg",
                  use_column_width=True)
    
    st.subheader("Abordagem do produto")
    texto2 = """Este produto busca trazer de maneira simples e prática a possibilidade de aplicação do
             método AHP. Para tal, precisamos conhecer os passos a serem seguidos e as características
             do modelo."""
    st.write(f'<div style="text-align: justify">{texto2}</div>', unsafe_allow_html=True)
    st.image("fluxo.jpg")
    
    texto3 = """Com isso, após definirmos quais as alternativas temos, precisamos pontuar quais os critérios
             adotados na tomada de decisão, bem como seu tipo (quantitativo ou qualitativo) e sua característica
             em relação ao negócio (a variação deste critério para mais ou para menos é prejudicial ou benéfica para
             sua tomada de decisão?). Em seguida, há a definição da matriz de julgamento, que é utilizada (seja olhando
             para uma variável qualitativa, seja olhando para todos os critérios) para que o tomador de decisão possa
             mensurar e dar pesos ao critério de acordo com sua respectiva importância. À medida que o número de critérios
             aumenta, a chance de os pesos apontados perderem sentido real aumenta. Para isso, há um teste de consistência, que
             verifica se as ponderações realizadas pelo tomador de decisão possuem sentido. Os diferentes pesos que podemos atribuir no
             relacionamento entre critérios seguem a escala fundamental de Saaty (imagem ao lado)"""
    st.write(f'<div style="text-align: justify">{texto3}</div>', unsafe_allow_html=True)
   
    st.image("escala_saaty.jpg", use_column_width=True)

    texto4 = """Por fim, vale comentar que o modelo possui a limitação de lidar com no máximo 15 critérios. Além disso,
             o número de combinações na matriz de julgamento aumenta conforme a expressão:
             """
    st.write(f'<div style="text-align: justify">{texto4}</div>', unsafe_allow_html=True)
    st.write("""
             $$
             \dfrac{n * (n - 1)}{2}
             $$
             Em que n é o número de critérios.""")
# Estrutura dedicada a receber as alternativas de solução do modelo
with st.container():
    st.title("Adição de alternativas")
    for row in st.session_state["alternativas"]:
        row_data = coordena_coleta.generate_row(row, "alternativas")
        rows_collection_alt.append(row_data)

    menu = st.columns(2)

    with menu[0]:
        # Botão que adiciona uma linha para receber mais uma alternativa
        st.button("Add Alternativa", on_click=coordena_coleta.add_row,  args=["alternativas"])
    with menu[1]:
        # Botão que indica que o processo foi finalizado
        st.button("Alternativas - Concluído", on_click=botoes.click_button_alternativas_concluidas)
    # Apresentação das alternativas coletadas
    if len(rows_collection_alt) > 0:
        st.subheader("Dados coletados - Alternativas")
        display = st.columns(1)
        data_alternativas = pd.DataFrame(rows_collection_alt)
        data_alternativas.rename(columns={"name": "alternativas"}, inplace=True)
        display[0].dataframe(data=data_alternativas, use_container_width=True)

# Estrutura dedicada ao recebimento dos critérios
with st.container():
    if st.session_state.alternativas_concluidas:
        st.title("Adição de critérios")

        for row in st.session_state["criterios"]:
            row_data = coordena_coleta.generate_row(row, "criterios")
            rows_collection_cri.append(row_data)

        menu = st.columns(2)

        with menu[0]:
            # Botão que indica que queremos adicionar mais um critério para escolha
            st.button("Add Critério", on_click=coordena_coleta.add_row,  args=["criterios"])
        with menu[1]:
            # Botão que indica que o processo de inserção de critérios foi finalizado
            st.button("Critério - Concluído", on_click=botoes.click_button_criterios_concluidos)
        # Apresentação dos dados coletados
        if len(rows_collection_cri) > 0:
            st.subheader("Dados coletados - Critérios")
            display = st.columns(1)
            data_criterios = pd.DataFrame(rows_collection_cri)
            data_criterios.rename(columns={"name": "criterios"}, inplace=True)
            data_criterios["caracteristica"] = data_criterios["caracteristica"].apply(lambda x: -1 if x == "Quanto maior, pior" else 1)
            display[0].dataframe(data=data_criterios, use_container_width=True)
            df_criterios_qualitativos = data_criterios[data_criterios["tipo"] == "qualitativo"].copy()

# Estrutura destinada ao tratamento de critérios qualitativos
with st.container():
    if st.session_state.criterios_concluidos:
        if len(df_criterios_qualitativos) > 0:
            st.title("Tratamento de critérios qualitativos")
            # Dicionário destinado a armazenar os pesos resultantes de cada qualidade de cada critério
            # qualitativo informado
            dict_quali_to_quanti = {}
            # Looping que percorre os critérios qualitativos para construção de sua respectiva
            # matriz de julgamento
            for criterio in df_criterios_qualitativos["criterios"]:
                st.subheader(f"Tratamento do critério: {criterio}")
                if f"criterios_quali_{criterio}" not in st.session_state:
                    st.session_state[f"criterios_quali_{criterio}"] = []
                
                if f"consistencia_quali_{criterio}" not in st.session_state:
                    st.session_state[f"consistencia_quali_{criterio}"] = False

                row_collection_cri_ql = []
                dict_quali_to_quanti[criterio] = {}
                for row in st.session_state[f"criterios_quali_{criterio}"]:
                    row_data = coordena_coleta.generate_row(row, f"criterios_quali_{criterio}")
                    row_collection_cri_ql.append(row_data)

                menu = st.columns(2)

                with menu[0]:
                    # Botão que indica que queremos adicionar mais um valor para o critério
                    st.button("Add Valor", on_click=coordena_coleta.add_row,  args=[f"criterios_quali_{criterio}"], key=uuid.uuid4())
                
                with menu[1]:
                    # Valores que indicam que a inserção de valores foi concluída
                    st.button(f"Valores concluídos para o critério {criterio}", on_click=botoes.click_button_criterio_quali_concluido,  args=[f"criterio_quali_concluido"], key=uuid.uuid4())
                
                if len(row_collection_cri_ql) > 0:
                    valores = [valor["name"] for valor in row_collection_cri_ql]
                    data_criterios_ql = df_opps.create_dataframe_from_list(valores)
                    st.subheader(f"Dados coletados - critério: {criterio}")
                    display = st.columns(1)
                    # Criação da matriz de julgamento para o(s) critério(s) qualitativo(s)
                    if st.session_state[f"criterio_quali_concluido"]:
                        data_criterios_ql_final = df_opps.create_judgement_table(data_criterios_ql, criterio)
                        display[0].dataframe(data=data_criterios_ql_final, use_container_width=True)
                        matrix_judge = data_criterios_ql_final.values
                        mj = ahp.MatrizJulgamento()
                        vetor_prioridade_criterio = mj.normalizacao_julgamentos(matrix_judge)
                        botao_consistencia = st.columns(1)
                        with botao_consistencia[0]:
                            # Botão que solicita a checagem de consistência para o critério em questão
                            st.button(f"Verificar consistência para o critério {criterio}", on_click=botoes.click_button_consistencia_quali,  args=[f"consistencia_quali_{criterio}"], key=uuid.uuid4())
                        if st.session_state[f"consistencia_quali_{criterio}"]:
                            cr_criterio = mj.analise_consistencia(matrix_judge, vetor_prioridade_criterio)
                            if cr_criterio > 10:
                                message = f"""O teste de consistência da matriz de julgamento reprovou as prioridades definidas.\n
                                            O resultando da razão de consistência deve ser menor que 10%. O valor encontrado foi
                                            {cr_criterio}"""
                                raise ValueError(message)
                            else:
                                st.write(f"Pesos atribuídos aprovados para o critério {criterio}")
                        for i in range(len(valores)):
                            dict_quali_to_quanti[criterio][valores[i]] = vetor_prioridade_criterio[i][0]
            menu_final = st.columns(1)
            with menu_final[0]:
                # Botão que indica que o processo para critérios qualitativos foi encerrado
                st.button("Tratamento encerrado para critérios qualitativos", on_click=botoes.click_button_criterios_quali_fim, key=uuid.uuid4())

# Estrutura dedicada a construir a matriz de julgamento do processo (considerando todos os critérios)
with st.container():
    if st.session_state["criterios_quali_finalizados_por_completo"] or (st.session_state.criterios_concluidos and len(df_criterios_qualitativos) == 0):
        if len(rows_collection_cri) > 0:
            valores = [valor["name"] for valor in rows_collection_cri]
            df_criterios_mapeados = df_opps.create_dataframe_from_list(valores)
            st.subheader("Dados coletados - Matriz de Julgamento")
            display = st.columns(1)
            df_julgamento = df_opps.create_judgement_table(df_criterios_mapeados, "criterio")
            display[0].dataframe(data=df_julgamento, use_container_width=True)
            matriz_julgamento = df_julgamento.values
            menu_final = st.columns(1)
            with menu_final[0]:
                # Botão que indica a finalização da matriz de julgamento
                st.button("Matriz de Julgamento Finalizada", on_click=botoes.click_button_matriz_julgamento, key=uuid.uuid4())

# Estrutura dedicada a construir a matriz de decisão
with st.container():
    if st.session_state["matriz_julgamento"]:
        if st.session_state["criterios_quali_finalizados_por_completo"]:
            df_decisao = df_opps.create_decision_table(data_alternativas, data_criterios, True, dict_quali_to_quanti)
        else:
            df_decisao = df_opps.create_decision_table(data_alternativas, data_criterios, False)

        st.subheader("Dados coletados - Matriz de Decisão")
        display = st.columns(1)
        display[0].dataframe(data=df_decisao, use_container_width=True)
        matriz_decisao = df_decisao.values
        menu_final = st.columns(1)
        with menu_final[0]:
            # Botão que indica a finalização da matriz de decisão
            st.button("Matriz de Decisão Finalizada", on_click=botoes.click_button_matriz_decisao, key=uuid.uuid4())

# Estrutura dedicada a execução do algoritmo e apresentação de resultados
with st.container():
    if st.session_state["matriz_decisao"]:
        lista_referencia = list(data_criterios["caracteristica"])
        process = ahp.AHP(matriz_julgamento = matriz_julgamento, matriz_decisao = matriz_decisao, lista_referencia_monotomica = lista_referencia)
        result = process.executa_algoritmo()
        df_results = data_alternativas.copy()
        df_results["resultados"] = result.flatten()
        max = df_results["resultados"].max()
        min = df_results["resultados"].min()
        st.subheader("Resultados - Verde (melhor escolha), Amarelo (valores intermediários), Vermelho (pior escolha)")
        display = st.columns(1)
        display[0].dataframe(df_results.style.apply(lambda x: df_opps.color_coding(row = x, max = max, min = min), axis=1))
