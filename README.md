## GenAI RAG Demo

This demo use RAG (Retrieval-Augmented Generation) engine based on deep document understanding. 
It offers a simple straight webui use [streamlit](https://streamlit.io/), combining LLM (Large Language Models) for businesses of providing financial report insights.

This repository contains **Dockerfile** of [Python](https://www.python.org/) for [Docker](https://www.docker.com/)'s [automated build](https://hub.docker.com/_/python/) published to the public [Docker Hub Registry](https://registry.hub.docker.com/).

### Config
Edit <b>config.yaml</b> and input values for <code>base_url</code>, <code>api_key</code>.


### Launching 

1. Launching with local python


```bash
cd genai_rag_demo
pip install -r requirements.txt
streamlit run genai_tool.py
```

2. Launching with docker


```bash
cd genai_rag_demo
docker build -t genai-rag-demo .
docker run -p 8501:8501 genai-rag-demo bash start.bash
```


