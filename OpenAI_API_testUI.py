import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="OpenAI API 接続テスト", page_icon="💬")

st.title("💬 OpenAI API チャットテスト")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY が設定されていません！Azure App Service の環境変数を確認してください。")
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "こんにちは。OpenAI APIの接続テスト用チャットです。"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("メッセージを入力してください")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("生成中..."):
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ],
            )
            answer = response.output_text
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})