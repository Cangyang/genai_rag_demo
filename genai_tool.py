import streamlit as st
import time
import os
from utils import get_config_val,get_operating_system_name
from doc_loader import load_document,save_uploaded_file
from rag import RagProcess

st.title("Financial Report Assistant")
model = st.selectbox("Select a model", get_config_val('name_list', 'model'))
temperature = st.slider("Temperature", 0.0, 2.0, 0.2)

doc_path = ""
sys_name = get_operating_system_name()
uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
if uploaded_file is not None:
    st.write("file name:", uploaded_file.name)
    st.write("file size:", uploaded_file.size, " byte")
    with st.spinner("Processing PDF..."):
        cache_path = get_config_val('win_file_path', 'cache') if sys_name == 'Windows' else get_config_val('linux_file_path', 'cache')
        os.makedirs(cache_path, exist_ok=True)
        doc_path = save_uploaded_file(uploaded_file, cache_path)
    st.success("Doc Process Done!")
    

system_prompt = st.text_area(value = load_document("system_prompts.txt"), label="system_prompt")
user_prompt = st.text_area(value = load_document("user_prompts.txt"), label="user_prompt")


if st.button("run"):
    with st.spinner("Answering..."):
        start = time.time()
        rag = RagProcess(doc_path, model, temperature, system_prompt, user_prompt)
        answer = rag.run()
        end = time.time()
        print(f"Got response from LLM API after {end - start}s elapsed ")
        st.markdown(answer)
    st.success("Done!")















