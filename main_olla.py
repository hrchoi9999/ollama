import os

import requests
import streamlit as st


DEFAULT_OLLAMA_URL = "https://applicable-explains-shirts-auditor.trycloudflare.com"


def get_default_ollama_url():
    try:
        secret_url = st.secrets.get("OLLAMA_BASE_URL")
    except Exception:
        secret_url = None

    return secret_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL)


st.set_page_config(page_title="Ollama_chat", page_icon="💬")

st.title("Ollama_chat")
st.caption("로컬 또는 외부 Ollama 서버를 이용한 생성형 대화 앱")

model_name = st.text_input("Ollama 모델", value="gemma4:latest")
base_url = st.text_input("Ollama 서버 주소", value=get_default_ollama_url())
max_tokens = st.slider("최대 답변 길이", min_value=20, max_value=1000, value=300, step=20)
user_message = st.text_area("질문을 입력하세요", height=160)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("답변 생성", type="primary"):
    if not user_message.strip():
        st.warning("질문을 입력해 주세요.")
    else:
        with st.spinner("Ollama가 답변을 생성하고 있습니다..."):
            try:
                payload = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": user_message}],
                    "stream": False,
                    "think": False,
                    "options": {"num_predict": max_tokens},
                }
                response = requests.post(
                    f"{base_url.rstrip('/')}/api/chat",
                    json=payload,
                    timeout=180,
                )
                response.raise_for_status()
                response_text = response.json()["message"]["content"]
                st.session_state.chat_history.insert(
                    0,
                    {
                        "question": user_message,
                        "answer": response_text,
                        "model": model_name,
                    },
                )
            except Exception as error:
                st.error("Ollama 서버에 연결하지 못했습니다.")
                st.info("Streamlit Cloud는 PC의 로컬 Ollama에 직접 접속할 수 없어서, 공개 접근 가능한 Ollama 서버 주소가 필요합니다.")
                st.caption(str(error))

if st.session_state.chat_history:
    st.subheader("대화 기록")
    for item in st.session_state.chat_history:
        st.markdown(f"**모델:** `{item['model']}`")
        st.markdown(f"**질문:** {item['question']}")
        st.markdown(f"**답변:** {item['answer']}")
        st.divider()
else:
    st.info("아직 대화 기록이 없습니다.")
