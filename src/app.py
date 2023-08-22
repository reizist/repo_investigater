import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage
from langchain.schema import AIMessage

from dotenv import load_dotenv
# 環境変数の読み込み
load_dotenv()

# ChatGPT-3.5のモデルのインスタンスの作成
chat = ChatOpenAI(model_name="gpt-3.5-turbo")

# セッション内に保存されたチャット履歴のメモリの取得
try:
    memory = st.session_state["memory"]
except:
    memory = ConversationBufferMemory(return_messages=True)

# チャット用のチェーンのインスタンスの作成
chain = ConversationChain(
    llm=chat,
    memory=memory,
)

# Streamlitによって、タイトル部分のUIをの作成
st.title("Chatbot in Streamlit")
history = []

try:
    history = memory.load_memory_variables({})["history"]
except Exception as e:
    st.error(e)

def clear_text():
    # ChatGPTの実行
    chain(text_input)

    # セッションへのチャット履歴の保存
    st.session_state["memory"] = memory

    # チャット履歴（HumanMessageやAIMessageなど）の読み込み
    try:
        history = memory.load_memory_variables({})["history"]
    except Exception as e:
        st.error(e)
    st.session_state["text"] = ""


text_input = st.text_input("Enter your message", key="text")
send_button = st.button("Send", on_click=clear_text)



# チャット履歴の表示
for index, chat_message in enumerate(history):
    if type(chat_message) == HumanMessage:
        message(chat_message.content, is_user=True, key=2 * index)
    elif type(chat_message) == AIMessage:
        message(chat_message.content, is_user=False, key=2 * index + 1)