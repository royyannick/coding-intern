import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from io import StringIO


PROMPT_EXPLAIN_CODE = "Can you explain what this Python code does by providing a bullet list: \n"
PROMPT_OPTIMIZE_CODE = "Can you optimize code for readability, without losing on perfomance. Please re-write the whole code with a cleaner and easier to read version. Make sure it adheres to PEP8 standards. Please do not add any header to your response just return the code so I can copy/paste it as is. \n"
PROMPT_COMMENT_CODE = "Please re-write the whole code with comments according to PEP8 standard. Do not change the behaviour of the code, just add the proper comments. Do not over-comment for no reason. Please do not add any header to your response just return the code so I can copy/paste it as is. \n"

# ============================================================
# Functions
# ============================================================
def generate_response(prompt, openai_api_key=None):
    if not openai_api_key:
        st.sidebar.error("Please add your OpenAI API key to continue.")
        return None

    llm = OpenAI(model_name=st.session_state["openai_model"], temperature=0.7, max_tokens=2500, openai_api_key=openai_api_key)
    return llm(prompt)

# ============================================================
# Streamlit UI
# ============================================================
st.title("🦜 Yannick's Coding Intern 🔗")

if "uploaded_code" not in st.session_state:
    st.session_state["uploaded_code"] = None

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.selectbox("OpenAI Model", ["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-instruct", "davinci"], key="openai_model")
    #"[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    uploaded_file = st.file_uploader("Upload a Python File", type=["py"])
    if uploaded_file:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        uploaded_code = stringio.read()
        st.session_state["uploaded_code"] = uploaded_code
        st.session_state["new_code"] = None
    st.markdown("---")

with st.expander("Uploaded Code", expanded=(uploaded_file is not None)):
    if uploaded_file:
        st.code(uploaded_code, language="python")
    else:
        st.warning("Please upload your code (.py file) via the side panel.")

col1, _, col2, _, col3 = st.columns([2,1,2,1,2])
main_response_view = st.empty()
main_response_button = st.empty()

with col1:
    explain_code = st.button("Explain Code", key="explain_code", disabled=(st.session_state["uploaded_code"] is None), use_container_width=True)
    if explain_code:
        prompt = PROMPT_EXPLAIN_CODE + st.session_state["uploaded_code"]
        main_response_view.info(generate_response(prompt, openai_api_key))
with col2:
    optimize_code = st.button("Optimize Code", key="optimize_code", disabled=(st.session_state["uploaded_code"] is None), use_container_width=True)
    if optimize_code:
        prompt = PROMPT_OPTIMIZE_CODE + st.session_state["uploaded_code"]
        with st.sidebar:
            with st.spinner("Intern working hard..."):
                st.session_state["new_code"] = generate_response(prompt, openai_api_key)
                main_response_view.code(st.session_state["new_code"])
                main_response_button.download_button(
                        label="Download Optimized Code",
                        data=st.session_state["new_code"],
                        file_name="optimized_code.py",
                        mime="text/plain",
                        use_container_width=True)
                st.success("Intern Assignment Completed!")

with col3:
    comment_code = st.button("Comment Code", key="comment_code", disabled=(st.session_state["uploaded_code"] is None), use_container_width=True)
    if comment_code:
        prompt = PROMPT_COMMENT_CODE + st.session_state["uploaded_code"]
        with st.sidebar:
            with st.spinner("Intern working hard..."):
                st.session_state["new_code"] = generate_response(prompt, openai_api_key)
                main_response_view.code(st.session_state["new_code"])
                main_response_button.download_button(
                        label="Download Commented Code",
                        data=st.session_state["new_code"],
                        file_name="commented_code.py",
                        mime="text/plain",
                        use_container_width=True)
                st.success("Intern Assignment Completed!")