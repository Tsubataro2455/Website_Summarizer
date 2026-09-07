import streamlit as st
from streamlit_chat import message
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def init_page():
    st.set_page_config(
        page_title="Website Summarizer",
        page_icon="🤗"
    )
    st.header("Website Summarizer 🤗")
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.costs = []


def select_model():
    model = st.sidebar.radio("Choose a model:", ("claude-haiku-4-5", "claude-sonnet-4-6"))
    if model == "claude-haiku-4-5":
        model_name = "claude-haiku-4-5"
    else:
        model_name = "claude-sonnet-4-6"

    return ChatAnthropic(model=model_name, temperature=0)

def get_url_input():
    url = st.text_input("URL: ", key="input")
    return url


def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_content(url):
    try:
        with st.spinner("Fetching Content ..."):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # fetch text from main (change the below code to filter page)
            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            else:
                return soup.body.get_text()
    except:
        st.write('something wrong')
        return None


def build_prompt(content, n_chars=300):
    return f"""以下はとある。Webページのコンテンツである。内容を{n_chars}程度でわかりやすく要約してください。

========

{content[:1000]}

========

日本語で書いてね！
"""


def main():
    # ページ設定
    init_page()

    # サイドバーの各種設定
    model = select_model()
    init_messages()

    # コンテナ情報の初期設定
    container = st.container()
    response_container = st.container()

    with container:
        # ユーザーから入力されたURL情報を取得し、構成要素を解析
        url = get_url_input()
        is_valid_url = validate_url(url)
        if not is_valid_url:
            st.write('Please input valid url')
            answer = None
        else:
            # 入力されたURLからページ情報を取得
            content = get_content(url)
            if content:
                # プロンプトを構築し、webサイトの要約を依頼
                prompt = build_prompt(content)
                st.session_state.messages.append(HumanMessage(content=prompt))
                with st.spinner("ChatGPT is typing ..."):
                    res = model.invoke(input=st.session_state.messages)
                    answer = res.content
                # st.session_state.costs.append(cost)
            else:
                answer = None

    if answer:
        with response_container:
            st.markdown("## Summary")
            st.write(answer)
            st.markdown("---")
            st.markdown("## Original Text")
            st.write(content)

if __name__ == '__main__':
    main()