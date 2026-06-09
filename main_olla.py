import streamlit as st
from langchain_ollama import ChatOllama


st.set_page_config(page_title="Ollama 생성형 대화 앱", page_icon="💬")

st.title("Ollama 생성형 대화 앱")

model_name = st.text_input("Ollama 모델", value="gemma4:latest")
user_message = st.text_area("질문을 입력하세요", height=160)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("답변 생성", type="primary"):
    if not user_message.strip():
        st.warning("질문을 입력해 주세요.")
    else:
        with st.spinner("Ollama가 답변을 생성하고 있습니다..."):
            chat_model = ChatOllama(model=model_name)
            response = chat_model.invoke(user_message)
            st.session_state.chat_history.insert(
                0,
                {
                    "question": user_message,
                    "answer": response.content,
                    "model": model_name,
                },
            )

if st.session_state.chat_history:
    st.subheader("대화 기록")
    for item in st.session_state.chat_history:
        st.markdown(f"**모델:** `{item['model']}`")
        st.markdown(f"**질문:** {item['question']}")
        st.markdown(f"**답변:** {item['answer']}")
        st.divider()
else:
    st.info("아직 대화 기록이 없습니다.")
