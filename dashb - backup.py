import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import requests
import io


#@st.cache
def indice():
    url_index = 'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/index.csv'
    fil = requests.get(url_index).content
    df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
    return list(df['ficha'])


#@st.cache
def git_busca(nome):
    index = str(nome)
    url_index = f'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/{index}.csv'
    fil = requests.get(url_index).content
    df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
    return df


def div():
    main = st.markdown(f"""<div style="background-color:#C29CFF;padding:5px;font-family:;
            width:100%">
            <h2 style="color:white;text-align:center;">Dashboard - Bioterio</h2>
            </div>""", unsafe_allow_html=True)
    st.text('')
    return main


def agregado():
    agg = []
    fichas = indice()
    for i in fichas:
        url_index = f'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/{str(i)}.csv'
        fil = requests.get(url_index).content
        df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
        agg.append(df['Total'].sum())
        print(agg)
    return agg


def painel():
    forma_1 = st.sidebar.form(key='form-1')
    forma_1.markdown("**Inventario**")
    #indexs = indice()
    select_box = forma_1.selectbox(label='', options=indice())
    sub = forma_1.form_submit_button('---ver---')
    if sub:
        df = git_busca(select_box)
        beta, gama, zeta = st.beta_columns(3)

        tot = df['Total'].sum()
        fem = df['Femeas'].sum()
        mach = df['Machos'].sum()
        cria = df['Crias'].sum()
        width = 100

        titulo = f"""<div style="background-color:#33F65C;padding:5px;border-radius:7px;font-family:
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

        gama.markdown(titulo, True)
        gama.text('')
        gama.markdown(total, True)
        gama.text('')
        gama.markdown(femeas, True)
        gama.text('')
        gama.markdown(machos, True)
        gama.text('')
        gama.markdown(crias, True)

        fig = plt.figure(num=1, figsize=(8, 10), dpi=520)
        sns.barplot(data=df, x='Total', y='Gaiola', palette="mako_r")
        plt.ylabel('Gaiola', labelpad=12)
        plt.xlabel('Numero de Murganhos', labelpad=12)
        plt.style.use('fivethirtyeight')
        zeta.pyplot(fig, clear_figure=True)

        fig2 = plt.figure(figsize=(12, 8))
        plt.style.use('seaborn')
        plt.pie(x=[df['Machos'].sum(), df['Femeas'].sum(), df['Crias'].sum()], labels=['Macho', 'Femeas', 'Crias'],
                autopct='%1.1f%%', explode=[0.04, 0.04, 0.04], pctdistance=0.5)
        beta.pyplot(fig2, clear_figure=True)

        fig3 = plt.figure(figsize=(14, 4), dpi=420)
        totais = agregado()
        sns.lineplot(x=indice(), y=totais, color='#C29CFF')
        plt.fill_between(x=indice(), y1=totais,color='#FFC7B2')
        plt.style.use('ggplot')
        plt.ylabel('Numero de animais', labelpad=6)

        st.pyplot(fig3, clear_figure=True, use_container_width=True)

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
    div()
    painel()
