import streamlit as st
import pandas as pd
import requests
import base64
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

    main = f"""<div style="background-color:{cor};border-radius:{curva}px;padding:5px;font-family:arial;
            width:100%">
            <{h} style="color:white;text-align:center;">{texto}</{h}>
            </div>"""
    return main


def html_main_body(data_frame):
    # soma total de cada categoria no dataframe -- para o painel
    criotubos = len(data_frame['Isolado'])
    caixas = ceil(len(data_frame['Isolado'].unique())/25)
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


def Main_criobank():
    # side-bar label
    st.sidebar.markdown(div(h='h2', cor='#464e5F', curva=0, texto='Crio-Bank'), unsafe_allow_html=True)
    st.sidebar.text('')

    df = git_busca()
    dfi = git_index()
    lista_1 = list(dfi['Canister'].unique())
    lista_2 = list(dfi['Caixa'].unique())
    lista_3 = list(df['Isolado'].unique())

    # side-bar form, select-box, botao da form:

    # Form 1 - Caixas
    forma_1 = st.sidebar.form(key='form-1')
    forma_1.markdown("**Menu**")
    select_box_Canister = forma_1.selectbox(label='Canister', options=lista_1)
    select_box_Caixa = forma_1.selectbox(label='Caixa', options=lista_2)
    sub = forma_1.form_submit_button('---ver---')

    # Form 2 - Isolados
    forma_2 = st.sidebar.form(key='form-2')
    forma_2.markdown("**Isolados**")
    select_box_isolados = forma_2.selectbox(label='Isolados', options=lista_3)
    sub_2 = forma_2.form_submit_button('---ver---')

    # Condicoes da forms:
    # form-1:
    if sub:
        # dataframe filtring
        if select_box_Caixa == 'Todas':
            df_fitrado = df[df['Canister'] == select_box_Canister]
        else:
            df_fitrado = df[(df['Canister'] == select_box_Canister) & (df['Caixa'] == select_box_Caixa)]

        # Agregacao
        agg = df_fitrado.groupby('Isolado').agg({'Caixa': 'count', 'Isolado': 'count'})

        # html_body
        html_main_body(df_fitrado)
        st.text('') #espaco

        # cabecalho para o dataframe
        st.markdown(div(h='h5', cor='#464e5F', curva=0,
                        texto=f'Tabela com os dados do {select_box_Canister} | {select_box_Caixa}'),
                    True)
        st.text('')

        st.dataframe(df_fitrado, width=1000, height=430)
        st.dataframe(agg.T, width=1000, height=430)
        # csv = df.to_csv(index=False)
        # b64 = base64.b64encode(csv.encode()).decode()
        # download = f'<a href="data:file/csv;base64,{b64}" download="{str(select_box)}.csv">Download ficheiro csv</a>'
        # st.markdown(download, unsafe_allow_html=True)

    elif sub_2:
        df_fitrado = df[df['Isolado'] == select_box_isolados]
        agg = df_fitrado.groupby('Isolado').agg({'Caixa': 'count', 'Isolado': 'count'})

        # html_body
        html_main_body(df_fitrado)
        st.text('')

        # cabecalho para o dataframe
        st.markdown(div(h='h5', cor='#464e5F', curva=7, texto=f'Tabela com os dados do isolado {select_box_isolados}'), True)
        st.text('')
        st.dataframe(df_fitrado, width=1000, height=430)
        st.dataframe(agg, width=1000, height=430)

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
    Main_criobank()
    info()
