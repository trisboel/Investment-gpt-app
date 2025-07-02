import streamlit as st
import openai
import yfinance as yf

st.set_page_config(page_title="Investment Assistant", layout="centered")
st.title("💼 Investment Assistant")

openai.api_key = st.secrets["OPENAI_API_KEY"]

user_input = st.text_input("📩 Deine Frage (z. B. '500 € in Apple – was tun?'):")

def analyze_input(user_input):
    tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL", "META"]
    analysis = []

    for ticker in tickers:
        if ticker.lower() in user_input.lower() or ticker.replace(".", "").lower() in user_input.lower():
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            price = hist["Close"].iloc[-1]
            analysis.append(f"Aktienkurs {ticker}: {price:.2f} USD")

    prompt = f"""Du bist ein Investment-Analyst. Gib eine kurze, einfache Handlungsempfehlung (Kaufen, Halten, Verkaufen) basierend auf dem folgenden Nutzereingabe und aktuellen Kursen:

Nutzerfrage: {user_input}
Kurse: {', '.join(analysis)}

Antworte nur mit der Empfehlung und einer kurzen Begründung in maximal 3 Sätzen.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message["content"]

if st.button("🚀 Analysieren") and user_input:
    with st.spinner("Analysiere…"):
        result = analyze_input(user_input)
        st.success(result)
