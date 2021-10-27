import streamlit as st
import pandas as pd
import requests
from math import ceil
import io


def git_index():
    """funcao para buscar o arquivo index.csv  no github e retorna um dataframe"""

    url_index = f'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/crio_index.csv'
    fil = requests.get(url_index).content
    dfi = pd.read_csv(io.StringIO(fil.decode('utf-8')))
    return dfi


def git_busca():
    """funcao para buscar o arquivo criobank.csv  no github e retorna um dataframe"""
    url_index = f'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/criobank.csv'
    fil = requests.get(url_index).content
    df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
    return df


def div(h, cor, texto, curva):
    """funcao div - retorna uma string do texto HTML com propiedades
        ajustaveis(h-titulo(h1,h2)/paragrafo(p), cor, texto)"""

    main = f"""<div style="background-color:{cor};border-radius:{curva}px;padding-top:1.5%;padding-bottom:0.5%;font-family:arial;
            width:100%">
            <{h} style="color:white;text-align:center;">{texto}</{h}>
            </div>"""
    return main


def html_main_body(data_frame):
    # soma total de cada categoria no dataframe -- para o painel
    criotubos = len(data_frame['Isolado'])
    caixas = ceil(len(data_frame['Isolado'].unique()) / 25)
    isolados = len(data_frame['Isolado'].unique())
    width = 100

    # Estrutura em HTML/CSS do painel #33F65C '#c9ddc9' #99ff99
    numero_criotubo = f"""<div style="background-color:#464e5F;padding:2px;border-radius:7px;font-family: arial
                    ;width: {width}%"> 
                    <h5 style="color:white;text-align:center;"> Numero de criotubos </h5>
                    <h4 style="color:white;text-align:center;"> {criotubos} </h4>
                    </div>"""

    numero_caixa = f"""<div style="background-color:#464e5F;padding:2px;border-radius:7px;font-family: arial;
                    width: {width}%">
                    <h5 style="color:white;text-align:center;"> Numero de caixas:</h5>
                    <h4 style="color:white;text-align:center;"> {caixas} </h4>
                    </div>"""

    numero_isolado = f"""<div style="background-color:#464e5F;padding:2px;border-radius:7px;font-family: arial;
                    width: {width}%">
                    <h5 style="color:white;text-align:center;"> Numero de isolados:</h5>
                    <h4 style="color:white;text-align:center;"> {isolados} </h4>
                    </div>"""

    # integrado o HTML via markdown nas colunas
    beta, gama, zeta = st.columns(3)  # lay-out: 3-colunas
    beta.markdown(numero_criotubo, True)
    gama.markdown(numero_caixa, True)
    zeta.markdown(numero_isolado, True)


def main_criobank(df_fitrado=None):

    # side-bar label
    global select_box_cp, select_box_local, select_box_ano, select_box_resist, select_box_especie, sub_3, select_box_animal

    st.sidebar.markdown(div(h='h2', cor='#464e5F', curva=0, texto='Crio-Bank'), unsafe_allow_html=True)
    st.sidebar.text('')

    df = git_busca()
    dfi = git_index()
    lista_1 = list(dfi['Canister'].unique())
    lista_2 = list(dfi['Caixa'].unique())
    lista_3 = list(df['Isolado'].unique())
    lista_4 = list(df['Especie'].unique())
    lista_5 = list(df['Status_de_resistencia'].unique())
    lista_6 = list(df['Ano_de_criopreservacao'].unique())
    lista_7 = list(df['Local_de_colheita'].unique())
    lista_8 = list(df['Animal_de_colheita'].unique())
    lista_9 = list(df['Agente_crioprotector'].unique())
    # side-bar form, select-box, botao da form:

    # Form 1 - Caixas
    forma_1 = st.sidebar.form(key='form-1')
    forma_1.markdown("**Menu**")
    select_box_canister = forma_1.selectbox(label='Canister', options=lista_1)
    select_box_caixa = forma_1.selectbox(label='Caixa', options=lista_2)
    sub = forma_1.form_submit_button('---ver---')

    # Form 2 - Isolados
    forma_2 = st.sidebar.form(key='form-2')
    #forma_2.markdown("**Isolados**")
    select_box_isolados = forma_2.selectbox(label='Isolados', options=lista_3)
    sub_2 = forma_2.form_submit_button('---ver---')

    # Check-box - pesquisa profunda
    #marco = st.sidebar.checkbox(label='Pesquisa profunda (varios parametros)')
    select_box_cp = select_box_local = select_box_ano = select_box_resist = select_box_especie = select_box_animal = sub_3 = st.empty# solvinng escope issues

    # Form 3 - Isolados
    forma_3 = st.sidebar.form(key='form-3')
    exp = forma_3.expander('Pesquisa profunda')
    exp.markdown("**Filtrar os dados**")
    select_box_especie = exp.selectbox(label='Especie', options=lista_4)
    select_box_resist = exp.selectbox(label='Status de resistencia', options=lista_5)
    select_box_ano = exp.selectbox(label='Ano de criopreservacao', options=lista_6)
    select_box_local = exp.selectbox(label='Proveniencia', options=lista_7)
    select_box_animal = exp.selectbox(label='Animal de colheita', options=lista_8)
    select_box_cp = exp.selectbox(label='Crioprotector', options=lista_9)
    sub_3 = forma_3.form_submit_button('---ver---')

    # Condicoes da forms:
    # form-1:
    if sub:
        # dataframe filtring
        if select_box_caixa == 'Todas':
            df_fitrado = df[df['Canister'] == select_box_canister]
        else:
            df_fitrado = df[(df['Canister'] == select_box_canister) & (df['Caixa'] == select_box_caixa)]

        # Agregacao
        agg = df_fitrado.groupby('Isolado').agg({'Caixa': 'count', 'Isolado': 'count'})

        # html_body
        html_main_body(df_fitrado)
        st.text('')  # espaco

        # cabecalho para o dataframe
        st.markdown(div(h='h5', cor='#464e5F', curva=0,
                        texto=f'Tabela com os dados do {select_box_canister} | {select_box_caixa}'),
                    True)
        st.text('')

        st.dataframe(df_fitrado, width=1400, height=500)
        st.markdown(div(h='h6', cor='#464e5F', curva=0, texto=f'Resumo - Somatororio'),
                    True)
        st.dataframe(agg.T, width=1400, height=500)

    elif sub_2:
        df_fitrado = df[df['Isolado'] == select_box_isolados]
        agg = df_fitrado.groupby('Isolado').agg({'Caixa': 'count', 'Isolado': 'count'})

        # html_body
        html_main_body(df_fitrado)
        st.text('')

        # cabecalho para o dataframe
        st.markdown(div(h='h5', cor='#464e5F', curva=7, texto=f'Tabela com os dados do isolado {select_box_isolados}'),
                    True)
        st.text('')
        st.dataframe(df_fitrado, width=1400, height=500)
        st.markdown(div(h='h6', cor='#464e5F', curva=0, texto=f'Resumo - Somatororio'),
                    True)
        st.dataframe(agg.T, width=1400, height=500)

    elif sub_3:
        if select_box_especie == 'Todos':
            df_fitrado = df[(df['Status_de_resistencia'] == select_box_resist) & (
                    df['Ano_de_criopreservacao'] == select_box_ano) & (
                                     df['Local_de_colheita'] == select_box_local) & (
                                     df['Animal_de_colheita'] == select_box_animal) & (
                                     df['Agente_crioprotector'] == select_box_cp)]
        if select_box_resist == 'Todos':
            df_fitrado = df[
                (df['Especie'] == select_box_especie) & (df['Ano_de_criopreservacao'] == select_box_ano) & (
                        df['Local_de_colheita'] == select_box_local) & (
                        df['Animal_de_colheita'] == select_box_animal) & (
                        df['Agente_crioprotector'] == select_box_cp)]
        if select_box_ano == 'Todos':
            df_fitrado = df[
                (df['Especie'] == select_box_especie) & (df['Status_de_resistencia'] == select_box_resist) & (
                        df['Local_de_colheita'] == select_box_local) & (
                        df['Animal_de_colheita'] == select_box_animal) & (
                        df['Agente_crioprotector'] == select_box_cp)]
        if select_box_local == 'Todos':
            df_fitrado = df[
                (df['Especie'] == select_box_especie) & (df['Status_de_resistencia'] == select_box_resist) & (
                        df['Ano_de_criopreservacao'] == select_box_ano) & (
                        df['Animal_de_colheita'] == select_box_animal) & (
                        df['Agente_crioprotector'] == select_box_cp)]
        if select_box_animal == 'Todos':
            df_fitrado = df[
                (df['Especie'] == select_box_especie) & (df['Status_de_resistencia'] == select_box_resist) & (
                        df['Ano_de_criopreservacao'] == select_box_ano) & (
                        df['Local_de_colheita'] == select_box_local) & (
                        df['Agente_crioprotector'] == select_box_cp)]
        if select_box_cp == 'Todos':
            df_fitrado = df[
                (df['Especie'] == select_box_especie) & (df['Status_de_resistencia'] == select_box_resist) & (
                        df['Ano_de_criopreservacao'] == select_box_ano) & (
                        df['Local_de_colheita'] == select_box_local) & (
                        df['Animal_de_colheita'] == select_box_animal)]
        else:
            df_fitrado = df[
                (df['Especie'] == select_box_especie) & (df['Status_de_resistencia'] == select_box_resist) & (
                        df['Ano_de_criopreservacao'] == select_box_ano) & (
                        df['Local_de_colheita'] == select_box_local) & (
                        df['Animal_de_colheita'] == select_box_animal) & (
                        df['Agente_crioprotector'] == select_box_cp)]

        agg = df_fitrado.groupby('Isolado').agg(
            {'Caixa': 'count', 'Isolado': 'count', 'Especie': 'count', 'Status_de_resistencia': 'count'})

        # html_body
        html_main_body(df_fitrado)
        st.text('')

        # cabecalho para o dataframe
        st.markdown(div(h='h5', cor='#464e5F', curva=7, texto=f'Tabela com os dados do isolado {select_box_isolados}'),
                    True)
        st.text('')
        st.dataframe(df_fitrado, width=1400, height=500)
        st.markdown(div(h='h6', cor='#464e5F', curva=0, texto=f'Resumo - Somatororio'),
                    True)
        st.dataframe(agg.T, width=1400, height=500)
    else:
        st.markdown("""Todo o conteúdo registrado no inventário biológico do biotério encontra-se 
                sumarizado nesse Dashboard.
        
### **Como proceder ?**
- Para ver a informação: escolha a ficha (inventario) que deseja ver e pressione o botão “ver”
### **O que você vai encontrar ?**
- Todos os registros devidamente organizados
- Gráficos explicativos com base no número de animais:\n
        	- Percentagem de machos/ fêmeas / crias\n
        	- Número de animais por gaiola\n
        	- Numero total de animais por inventário\n  
        - Tabela do inventário e uma opção de download
        """)


def info():
    expander = st.sidebar.expander('Notas importantes')
    expander.markdown('**Informação**')
    expander.info("""- Para melhor exibição
                    Selecione: Settings->Appearence->Wide mode
                    - Para mudar o tema
                    selecione: Settings->Theme""")
    expander.warning("""- No telefone o dashboard pode 
                        aparecer mal enquadrado.
                        para solucionar,
                        dentro do seu navegador selecione 
                        a opção "vista para site de computador":   
                        - No Chrome: site para   computador;    
                        - No Opera: site no computador""")
    expander_2 = st.sidebar.expander('Sobre')
    expander_2.info("""- Criobank Monitor v.1.0 
                        Desenvolvido em Python 3 | Streamlit framework, et al|      
                        Dev: Edmilson Filimone
                        Correspondência: philimone99@gmail.com""")


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    st.markdown(div(h='h4', cor='#464e5F', curva=0, texto='Monitor do Banco de Isolados'), unsafe_allow_html=True)
    st.text('')
    main_criobank()
    info()
