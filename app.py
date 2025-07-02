import streamlit as st
from openai import OpenAI
import yfinance as yf

st.set_page_config(page_title="Investment GPT mit Echtzeit-Daten", page_icon="💹")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Investment GPT mit Echtzeit-Finanzdaten 🚀")
st.write("Frag mich, wie du am besten in Aktien oder ETFs investieren kannst.")

user_input = st.text_input("Gib deine Frage ein:", "")

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        last_close = hist['Close'][-1]
        prev_close = hist['Close'][-2]
        change = (last_close - prev_close) / prev_close * 100
        return {
            "ticker": ticker,
            "last_close": last_close,
            "change_percent": change
        }
    except Exception as e:
        return None

def analyze_input(user_input):
    # Beispiel: Wir suchen ein Ticker-Symbol in der Frage (sehr einfach)
    # Für eine richtige App sollte das besser gemacht werden
    tickers = ["AAPL", "MSFT", "TSLA", "GOOG", "AMZN"]  # Beispiel
    found_ticker = None
    for t in tickers:
        if t.lower() in user_input.lower():
            found_ticker = t
            break

    stock_info_text = ""
    if found_ticker:
        data = fetch_stock_data(found_ticker)
        if data:
            stock_info_text = f"Die aktuelle Schlusskurs von {data['ticker']} ist {data['last_close']:.2f} USD, mit einer Tagesänderung von {data['change_percent']:.2f}%. "
        else:
            stock_info_text = f"Leider konnte ich keine aktuellen Daten für {found_ticker} abrufen. "

    prompt = stock_info_text + "Basierend darauf, " + user_input

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        result = response.choices[0].message.content
        return result
    except Exception as e:
        return f"Fehler bei der Anfrage an OpenAI: {e}"

if user_input:
    with st.spinner("Analysiere deine Anfrage..."):
        answer = analyze_input(user_input)
    st.markdown(f"**Antwort:** {answer}")
