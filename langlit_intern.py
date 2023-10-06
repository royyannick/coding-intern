import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from io import StringIO


# ============================================================
# Functions
# ============================================================
def generate_response(prompt, openai_api_key=None):
    if not openai_api_key:
        st.sidebar.error("Please add your OpenAI API key to continue.")
        return None

    llm = OpenAI(temperature=0.7, max_tokens=1000, openai_api_key=openai_api_key)
    return llm(prompt)


# ============================================================
# Streamlit UI
# ============================================================
st.title("🦜 Yannick's Coding Intern 🔗")

if "uploaded_code" not in st.session_state:
    st.session_state["uploaded_code"] = None

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", value="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", type="password")
    #"[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    uploaded_file = st.file_uploader("Upload a Python File", type=["py"])
    if uploaded_file:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        uploaded_code = stringio.read()
        st.session_state["uploaded_code"] = uploaded_code

with st.expander("Uploaded Code"):
    if uploaded_file:
        st.code(uploaded_code, language="python")
    else:
        st.warning("Please upload your code (.py file) via the side panel.")

col1, _, col2, _, col3 = st.columns([2,1,2,1,2])
main_response_view = st.empty()
main_response_button = st.empty()

with col1:
    explain_code = st.button("Explain Code", key="explain_code", disabled=(st.session_state["uploaded_code"] is None))
    if explain_code:
        prompt = "Can you explain what this python code does: \n" + st.session_state["uploaded_code"]
        main_response_view.info(generate_response(prompt, openai_api_key))
with col2:
    optimize_code = st.button("Optimize Code", key="optimize_code", disabled=(st.session_state["uploaded_code"] is None))
    if optimize_code:
        prompt = "Can you optimize this code? Please re-write the whole optimized version. \n" + st.session_state["uploaded_code"]
        with st.sidebar:
            with st.spinner("Intern working hard..."):
                main_response_view.code(generate_response(prompt, openai_api_key))
                if main_response_button.button("Export Optimized Code"):
                    st.download_button(
                        label="Download Optimized Code",
                        data=main_response_view.code,
                        file_name="optimized_code.py",
                        mime="text/plain"
                    )
                st.success("Intern Assignment Completed!")

with col3:
    comment_code = st.button("Comment Code", key="comment_code", disabled=(st.session_state["uploaded_code"] is None))
    if comment_code:
        prompt = "Can you comment this code? Please re-write the whole code with comments according to PEP8 standard. \n" + st.session_state["uploaded_code"]
        main_response_view.code(generate_response(prompt, openai_api_key))
