import os

import streamlit as st
from langchain_ollama import ChatOllama


DEFAULT_OLLAMA_URL = "http://localhost:11434"


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
user_message = st.text_area("질문을 입력하세요", height=160)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("답변 생성", type="primary"):
    if not user_message.strip():
        st.warning("질문을 입력해 주세요.")
    else:
        with st.spinner("Ollama가 답변을 생성하고 있습니다..."):
            try:
                chat_model = ChatOllama(model=model_name, base_url=base_url)
                response = chat_model.invoke(user_message)
                st.session_state.chat_history.insert(
                    0,
                    {
                        "question": user_message,
                        "answer": response.content,
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
