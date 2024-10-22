import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Configuração da página
st.set_page_config(page_title='Painel de Ações da B3', layout='wide')

# Título centralizado usando HTML
st.markdown("<h1 style='text-align: center; color: #1ED760;'>PREÇO DE FECHAMENTO E DIVIDENDOS DE AÇÕES DA B3</h1>", unsafe_allow_html=True)

# Input do usuário
tickers = st.multiselect('Digite os tickers das ações para análise', ['BBSE3', 'WEGE3', 'TGAR11', 'MXRF11', 'DEVA11', 'XPML11'], default=['WEGE3'])

# Seletor deslizante para o período
period = st.select_slider('Selecione o período', options=['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], value='1y')

# Loop para cada ticker selecionado
for ticker in tickers:
    empresa = yf.Ticker(f"{ticker}.SA")
    try:
        # Obter histórico de preços
        tickerDF = empresa.history(period=period)

        # Verificar se o DataFrame não está vazio
        if not tickerDF.empty:
            # Cálculo das médias móveis
            tickerDF['SMA_50'] = tickerDF['Close'].rolling(window=50).mean()
            # tickerDF['SMA_200'] = tickerDF['Close'].rolling(window=200).mean()

            # Layout das informações da empresa
            st.subheader(f"Análise da Ação: {ticker}")
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.write(f"**Empresa:** {empresa.info.get('longName', 'Não disponível')}")

            with col2:
                st.write(f"**Mercado:** {empresa.info.get('industry', 'Não disponível')}")

            with col3:
                # Obtém o último preço de fechamento do histórico se disponível
                ultimo_preco = tickerDF['Close'].iloc[-1] if 'Close' in tickerDF.columns else 'Não disponível'
                st.write(f"**Preço Atual: R$** {ultimo_preco:.2f}")

            # Gráfico interativo com Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=tickerDF.index, y=tickerDF['Close'], mode='lines', name='Fechamento'))
            fig.add_trace(go.Scatter(x=tickerDF.index, y=tickerDF['SMA_50'], mode='lines', name='Média Móvel 50'))
            # fig.add_trace(go.Scatter(x=tickerDF.index, y=tickerDF['SMA_200'], mode='lines', name='Média Móvel 200'))
            fig.update_layout(title=f'Preço de Fechamento e Médias Móveis - {ticker}', xaxis_title='Data', yaxis_title='Preço (R$)')
            st.plotly_chart(fig)

            # Gráfico de Dividendos
            st.bar_chart(tickerDF['Dividends'], use_container_width=True)

            # Download de dados como CSV
            csv = tickerDF.to_csv().encode('utf-8')
            st.download_button(
                label=f"Baixar dados em CSV - {ticker}",
                data=csv,
                file_name=f'{ticker}_historico.csv',
                mime='text/csv',
            )

            # Notificação de preço
            preco_alerta = st.number_input(f"Defina um preço de alerta para {ticker}", value=0.0)
            if ultimo_preco >= preco_alerta > 0:
                st.success(f"O preço da ação {ticker} atingiu o valor de alerta definido: R$ {preco_alerta:.2f}")
        else:
            st.write(f"**Não foram encontrados dados para o ticker {ticker}.**")

    except Exception as e:
        st.write(f"**Erro ao obter dados para o ticker {ticker}. Tente novamente mais tarde.**")
        st.write(f"**Detalhes do erro:** {e}")
