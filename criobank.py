import streamlit as st
import pandas as pd
from PIL import Image
import requests
from math import ceil
import io
from functools import reduce


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


def logo():
    col1, col2, col3 = st.sidebar.columns(3)
    url = 'https://github.com/Edmilson-Filimone/datasets/raw/main/logo.png'
    pic_content = requests.get(url).content
    with open('image.png', 'wb') as file:
        foto = file.write(pic_content)
        file.close()

    pil = Image.open('image.png')
    col2.image(pil, use_column_width=True, clamp=True)
    col1.write('')


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
    caixas = ceil(len(data_frame['Isolado'])/25)
    isolados = len(data_frame['Isolado'].unique())
    width = 100

    # Estrutura em HTML/CSS do painel #33F65C '#c9ddc9' #99ff99 ##404340 ##464e5F #F4D44E
    numero_criotubo = f"""<div style="background-color:#464e5F;padding:2px;border-radius:7px;font-family: arial
                    ;width: {width}%"> 
                    <h6 style="color:white;text-align:center;"> Numero de criotubos </h6>
                    <h5 style="color:white;text-align:center;">{criotubos}</h5>
                    </div>"""

    numero_caixa = f"""<div style="background-color:#F4D44E;padding:2px;border-radius:7px;font-family: arial;
                    width: {width}%">
                    <h6 style="color:black;text-align:center;"> Numero de caixas</h6>
                    <h5 style="color:black;text-align:center;">{caixas}</h5>
                    </div>"""

    numero_isolado = f"""<div style="background-color:#4ADEDE;padding:2px;border-radius:7px;font-family: arial;
                    width: {width}%">
                    <h6 style="color:black;text-align:center;"> Numero de isolados </h6>
                    <h5 style="color:black;text-align:center;">{isolados}</h5>
                    </div>"""

    # integrado o HTML via markdown nas colunas
    beta, gama, zeta = st.columns(3)  # lay-out: 3-colunas
    beta.markdown(numero_criotubo, True)
    gama.markdown(numero_caixa, True)
    zeta.markdown(numero_isolado, True)


@st.cache
def download_button(data, nome):
    file = data.to_csv().encode('utf-8')

    st.download_button(label='Baixar os dados', data=file, file_name=nome, mime='csv')


def main_criobank():
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
    # forma_2.markdown("**Isolados**")
    select_box_isolados = forma_2.selectbox(label='Isolados', options=lista_3)
    sub_2 = forma_2.form_submit_button('---ver---')

    # Check-box - pesquisa profunda
    # marco = st.sidebar.checkbox(label='Pesquisa profunda (varios parametros)')
    select_box_cp = select_box_local = select_box_ano = select_box_resist = select_box_especie = select_box_animal = sub_3 = st.empty  # solvinng escope issues

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
            df_filtrado = df[df['Canister'] == select_box_canister]
        else:
            df_filtrado = df[(df['Canister'] == select_box_canister) & (df['Caixa'] == select_box_caixa)]

        # Agregacao
        #agg = df_filtrado.groupby('Isolado').agg({'Caixa': 'count', 'Isolado': 'count'})
        agg = df_filtrado['Isolado'].value_counts()

        # html_body
        html_main_body(df_filtrado)
        st.text('')  # espaco

        # cabecalho para o dataframe
        st.markdown(div(h='h6', cor='#464e5F', curva=0,
                        texto=f'Tabela com os dados do {select_box_canister} | {select_box_caixa}'),
                    True)
        st.text('')

        st.dataframe(df_filtrado, width=1400, height=500)
        st.markdown(div(h='h6', cor='#464e5F', curva=0, texto=f'Resumo - Somatororio'),
                    True)
        st.dataframe(agg.reset_index(), width=1400, height=200)
        download_button(data=df_filtrado, nome=f'Ficha_{select_box_canister}_{select_box_caixa}.csv')

    elif sub_2:
        df_filtrado = df[df['Isolado'] == select_box_isolados]
        agg = df_filtrado['Isolado'].value_counts()

        # html_body
        html_main_body(df_filtrado)
        st.text('')

        # cabecalho para o dataframe
        st.markdown(div(h='h5', cor='#464e5F', curva=7, texto=f'Tabela com os dados do isolado {select_box_isolados}'),
                    True)
        st.text('')
        st.dataframe(df_filtrado, width=1400, height=500)
        st.markdown(div(h='h6', cor='#464e5F', curva=0, texto=f'Resumo - Somatororio'),
                    True)
        st.dataframe(agg.T, width=1400, height=500)
        download_button(data=df_filtrado, nome=f'Ficha_{select_box_isolados}.csv')

    elif sub_3:
        # criando varios dataframes para cada pesquisa
        df1 = df.loc[df['Especie'] == select_box_especie.replace('Todos', '')]
        df2 = df.loc[df['Status_de_resistencia'] == select_box_resist.replace('Todos', '')]
        df3 = df.loc[df['Ano_de_criopreservacao'] == select_box_ano.replace('Todos', '')]
        df4 = df.loc[df['Local_de_colheita'] == select_box_local.replace('Todos', '')]
        df5 = df.loc[df['Animal_de_colheita'] == select_box_animal.replace('Todos', '')]
        df6 = df.loc[df['Agente_crioprotector'] == select_box_cp.replace('Todos', '')]

        colunas = ['Canister', 'Canister-Level', 'Caixa', 'Posicao do Criotubo', 'Isolado',
                         'Especie', 'Status_de_resistencia', 'Local_de_colheita',
                         'Animal_de_colheita', 'Ano_de_criopreservacao', 'Agente_crioprotector',
                         'Volume/tubo']

        colunas_x = ['Canister_x', 'Canister-Level_x', 'Caixa_x', 'Posicao do Criotubo_x', 'Isolado_x', 'Especie_x',
                     'Status_de_resistencia_x', 'Local_de_colheita_x', 'Animal_de_colheita_x', 'Ano_de_criopreservacao_x',
                     'Agente_crioprotector_x', 'Volume/tubo_x']

        # juntando todos os dataframes (pd.merge()) com base na coluna ID
        data_frames = [df1, df2, df3, df4, df5, df6]
        new_data = []

        for data in data_frames:
            if data.size > 0:
                new_data.append(data)

        print(new_data)

        # aglutinando os dataframes (funcao reduce e lambda para agrupar varios dataframes)
        # fonte: https://newbedev.com/merging-multiple-dataframes-in-pandas-code-example
        df_merged = reduce(lambda left, right: pd.merge(left, right, on=['id'], how='inner'), new_data)
        numero_de_colunas = len(df_merged.columns)

        df_merged.columns = [list(range(numero_de_colunas))]
        df_merged = df_merged[list(range(12))]
        df_merged.columns = colunas
        df_filtrado = df_merged

        #agg = df_filtrado.groupby('Isolado').agg({'Caixa': 'count', 'Isolado': 'count', 'Especie': 'count',
        #                                          'Status_de_resistencia': 'count'})
        agg = df_filtrado['Isolado'].value_counts()

        # html_body
        html_main_body(df_filtrado)
        st.text('')

        # cabecalho para o dataframe
        st.markdown(div(h='h5', cor='#464e5F', curva=7, texto=f'Tabela com os dados do isolado {select_box_especie}'),
                    True)
        st.text('')
        st.dataframe(df_filtrado, width=1400, height=500)
        st.markdown(div(h='h6', cor='#464e5F', curva=0, texto=f'Resumo - Somatororio'),
                    True)
        st.dataframe(agg.T, width=1400, height=500)
        download_button(data=df_filtrado, nome=f'Ficha_{select_box_especie}_filtro.csv' )
    else:
        st.markdown("""Todo o conteúdo registrado do banco de isolado de tripanossomas do CB-UEM encontra-se 
                sumarizado nesta Web-App.
        
### **Como proceder ?**
- Para ver a informação: escolha o conteúdo que deseja ver atraves dos submenus do painel e pressione o botão “ver”
### **O que você vai encontrar ?**
- Todos os registros devidamente organizados e sumarizados
- Três submenus para filtrar o conteudo:\n
- Um painel indicador\n
        - Número de caixas em uso\n
        - Número total de criotubos\n  
        - Número de isolados criopreservados
        """)


def info():
    expander = st.sidebar.expander('Notas importantes')
    expander.markdown('**Informação**')
    expander.info("""- Para mudar o tema
                    selecione: Settings->Theme""")
    expander.warning("""- No Mobile: selecione a opção "vista para site de computador":
    para melhor enquadramento""")
    expander_2 = st.sidebar.expander('Sobre')
    expander_2.info("""- Criobank Monitor v.1.0 
                        Desenvolvido em Python 3 | Streamlit framework, et al|      
                        Dev: Edmilson Filimone
                        Correspondência: philimone99@gmail.com""")


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    st.markdown(div(h='h5', cor='#464e5F', curva=0, texto='Painel do banco de isolados de tripanossoma'),
                unsafe_allow_html=True)
    st.text('')
    logo()
    main_criobank()
    info()
    # st.error('Oopahhh!!! Problemas com a rede...')
    # st.info('Tente novamente...')
    # st.info('Para suporte: philimone99@gmail.com')

# streamlit run G:\PyPrograms\CrioBank\criobank.py
