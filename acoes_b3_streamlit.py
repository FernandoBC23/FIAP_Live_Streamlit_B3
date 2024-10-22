import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title='Painel de Ações da B3',
    layout='wide'
)

st.header("**PAINEL DE PREÇO DE FECHAMENTO E DIVIDENDOS DE AÇÕES DA B3**")

# Input do usuário
ticker = st.text_input('Digite o ticker da ação', 'BBAS3')
empresa = yf.Ticker(f"{ticker}.SA")

try:
    # Obter histórico de preços (usando período de 5 anos para mais dados)
    tickerDF = empresa.history(period="5y")

    # Verificar se o DataFrame não está vazio
    if not tickerDF.empty:
        col1, col2, col3 = st.columns([1, 1, 1])

        # Informações da empresa com tratamento de erros
        with col1:
            st.write(f"**Empresa:** {empresa.info.get('longName', 'Não disponível')}")

        with col2:
            st.write(f"**Mercado:** {empresa.info.get('industry', 'Não disponível')}")

        with col3:
            # Obtém o último preço de fechamento do histórico se disponível
            ultimo_preco = tickerDF['Close'].iloc[-1] if 'Close' in tickerDF.columns else 'Não disponível'
            st.write(f"**Preço Atual: R$** {ultimo_preco:.2f}")

        # Exibir gráficos
        st.line_chart(tickerDF['Close'])
        st.bar_chart(tickerDF['Dividends'])
    else:
        st.write("**Não foram encontrados dados para o ticker informado.**")

except Exception as e:
    st.write("**Erro ao obter dados para o ticker informado. Tente novamente mais tarde.**")
    st.write(f"**Detalhes do erro:** {e}")
