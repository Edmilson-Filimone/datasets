import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import requests
import io


@st.cache
def indice():
    """funcao para buscar o arquivo index.csv no github, criar um dataframe e retornar uma lista com os dados
    da coluna 'ficha' que sao os nomes dos arquivos que serao usados adiante"""

    url_index = 'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/index.csv'
    fil = requests.get(url_index).content
    df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
    return list(df['ficha'])


@st.cache
def git_busca(nome):
    """funcao para buscar o arquivo csv (nome) no github e retorna um dataframe"""

    index = str(nome)
    url_index = f'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/{index}.csv'
    fil = requests.get(url_index).content
    df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
    return df


def div(h, cor, texto,curva):
    """funcao div - retorna uma string do texto HTML com propiedades ajustaveis(h-titulo(h1,h2)/paragrafo(p), cor, texto)"""

    main = f"""<div style="background-color:{cor};border-radius:{curva}px;padding:5px;font-family:;
            width:100%">
            <{h} style="color:white;text-align:center;">{texto}</{h}>
            </div>"""
    return main


def agregado():
    """Abre todos os arquivos csv no github cujos nomes estao na lista 'fichas (retornada pela funcao indice())
    E faz a soma da coluna 'total' de cada arquivo e adiciona na lista agg que sera usada no grafico cumulativo de
     linhas no dashboard'"""

    agg = []
    fichas = indice()
    for i in fichas:
        url_index = f'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/{str(i)}.csv'
        fil = requests.get(url_index).content
        df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
        agg.append(df['Total'].sum())
        print(agg)
    return agg


def dashboard():
    #side-bar, select-box, botao da form:
    forma_1 = st.sidebar.form(key='form-1')
    forma_1.markdown("**Inventario**")
    select_box = forma_1.selectbox(label='', options=indice())
    sub = forma_1.form_submit_button('---ver---')
    if sub:
        df = git_busca(select_box)

        #lay-out: 3-colunas
        beta, gama, zeta = st.beta_columns(3)
        beta.markdown(div(h='h3', cor='#464e5F', curva=7, texto='Balanco (%)'), True)
        zeta.markdown(div(h='h3', cor='#464e5F', curva=7, texto=f'Numero de animais ({select_box})'), True)

        #soma total de cada categoria no dataframe -- para o painel
        tot = df['Total'].sum()
        fem = df['Femeas'].sum()
        mach = df['Machos'].sum()
        cria = df['Crias'].sum()
        width = 100

        #Estrutura em HTML/CSS do painel #33F65C '#c9ddc9' #99ff99
        titulo = f"""<div style="background-color:#99ff99;padding:5px;border-radius:7px;font-family:
                ;width: {width}%"> 
                <h3 style="color:white;text-align:center;">Dados Gerais </h3>
                </div>"""

        total = f"""<div style="background-color:#464e5F;padding:5px;border-radius:7px;font-family: ;
                width: {width}%">
                <h3 style="color:white;text-align:left;"> Total: {tot}</h3>
                </div>"""

        femeas = f"""<div style="background-color:#464e5F;padding:5px;border-radius:7px;font-family:;
                width: {width}%">
                <h3 style="color:white;text-align:left;">Femeas: {fem}</h3>
                </div>"""

        machos = f"""<div style="background-color:#464e5F;padding:5px;border-radius:7px;font-family:;
                width: {width}%">
                <h3 style="color:white;text-align:left;">Machos: {mach} </h3>
                </div>"""

        crias = f"""<div style="background-color:#464e5F;padding:5px;border-radius:7px;font-family:
                width: {width}%">
                <h3 style="color:white;text-align:left;">Crias: {cria}</h3>
                </div>"""

        #integrado o HTML via markdown nas colunas
        gama.markdown(titulo, True)
        gama.text('')
        gama.markdown(total, True)
        gama.text('')
        gama.markdown(femeas, True)
        gama.text('')
        gama.markdown(machos, True)
        gama.text('')
        gama.markdown(crias, True)
        st.text('') #espacamento entre o painel e a figura

        #grafico de barras (coluna 3 -zeta)
        fig = plt.figure(num=1, figsize=(8, 10), dpi=520)
        sns.barplot(data=df, x='Total', y='Gaiola', palette="mako_r")
        plt.ylabel('Gaiola', labelpad=12)
        plt.xlabel('Numero de Murganhos', labelpad=12)
        plt.style.use('fivethirtyeight')
        zeta.pyplot(fig, clear_figure=True) #plotando

        #grafico de pizza (coluna 1 - beta)
        fig2 = plt.figure(figsize=(10, 8), dpi=520)
        plt.style.use('seaborn')
        plt.pie(x=[df['Machos'].sum(), df['Femeas'].sum(), df['Crias'].sum()], labels=['Macho', 'Femeas', 'Crias'],
        autopct='%1.1f%%', explode=[0.04, 0.04, 0.04], pctdistance=0.82, colors=['#66b3ff', '#ffcc99', '#c9ddc9'])
        plt.tight_layout()
        plt.legend()

        #convertendo pizza chart para donut chart
        centre_circle = plt.Circle((0, 0), 0.60, fc='white')
        fig_2 = plt.gcf()
        fig_2.gca().add_artist(centre_circle)
        beta.pyplot(fig2, clear_figure=True) #plotando

        # cabecalho para o grafico cumulativo de linhas
        st.markdown(div(h='h3', cor='#464e5F', curva=7, texto=' Variacao do numero de animais'), True)
        st.text('') #espacamento entre o cabecalho e a figura

        #grafico de linhas com o numero de murganhos de todas as fichas
        fig3 = plt.figure(figsize=(14, 4), dpi=420)
        totais = agregado()
        sns.lineplot(x=indice(), y=totais, color='#C29CFF', linewidth=1.8, marker='o', markersize=14, label='Numero de animais')
        #plt.fill_between(x=indice(), y1=totais, color='#FFC7B2')
        plt.style.use('ggplot')
        plt.legend()
        plt.ylabel('Numero de animais', labelpad=6)
        st.pyplot(fig3, clear_figure=True, use_container_width=True) #plotando

        # cabecalho para o dataframe
        st.markdown(div(h='h3', cor='#464e5F', curva=7, texto=f'Tabela com os dados do Inventario'), True)
        st.text('')

        #dataframe
        st.dataframe(df, width=1000, height=430)


def lay_2():
    global ficheiro, ficha_id, data
    forma_2 = st.sidebar.form(key='f2')
    forma_2.markdown('**Inserir Ficha**')
    passw = forma_2.text_input(label='Chave', type='password')
    sub2 = forma_2.form_submit_button('OK')
    if sub2:
        if passw == 'inventario':
            ficha_id = forma_2.text_input('Ficha-ID')
            data = forma_2.date_input('Data')
            ficheiro = forma_2.file_uploader('Documento', 'CSV')
            sub = forma_2.form_submit_button('Submeter')
            if sub:
                # query para inserir dados
                forma_2.success('Submetido com sucesso')
        else:
            forma_2.error('Acesso negado...')


ficha_id = ''
ficheiro = ''
data = ''

if __name__ == '__main__':
    st.markdown(div(h='h2', cor='#464e5F', curva=0, texto='Dashboard - Bioterio'), unsafe_allow_html=True)
    st.text('')
    dashboard()
