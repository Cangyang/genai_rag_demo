from langchain_community.embeddings import DashScopeEmbeddings
from doc_loader import load_document
# split plain text into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter 
import os
# vector store
import faiss
import numpy as np
from utils import get_config_val
from client import LLMClient


class RagProcess:

    def __init__(self, doc_path:str, model:str, temperature:float, system:str, user_query:str, top_k:int = 3):
        """
        Process: 
        1. loading embedding model
        2. split doc into chunks and embedding them
        3. embedding user query and search related chunks from index store
        4. call LLM model API and get response according to user query and related chunks 

        :param  doc_path: doc file path
        :param  mode: which llm model
        :param  temperature: what temperature llm model used
        :param  system: the system prompt that llm model used
        :param  user_query: the user prompt that llm model used
        :param  top_k: the most top k similar chunks for llm context, default is 3
        """

        self.doc_path = doc_path
        self.model = model
        self.temperature = temperature
        self.system = system
        self.user_query = user_query
        self.top_k = top_k
        config_api_key = get_config_val('api_key','model')
        self._api_key = config_api_key if config_api_key else os.getenv('api_key')
        print(self._api_key)
        self.embedding_model = self.load_embedding_model()


    def load_embedding_model(self):
        """
        loading text-embedding-v2 model
        return: loaded text-embedding-v2 model
        """
        embeding_model_name = get_config_val('embedding','model')
        print(f"loading Embedding: {embeding_model_name}...")

        embedding_model = DashScopeEmbeddings(
            model=embeding_model_name,
            dashscope_api_key=self._api_key
        )
        return embedding_model

    
    def indexing(self):
        """
        Process: loanding document and split text into chunks, embedding chunks and finally store them into vector db

        :return: index of embedding in faiss db and related chunks
        """
        all_chunks = []
        doc_text = load_document(self.doc_path)
        print(f"The total character size of doc: {self.doc_path} is: {len(doc_text)}")
        # config RecursiveCharacterTextSplitter to split text into chunks, each chunk has 512 characters and overlap is 128 characters
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048, chunk_overlap=512
        )
        
        # split text into chunks
        chunks = text_splitter.split_text(doc_text)
        print(f"The chunk size of the doc: {self.doc_path} is: {len(chunks)}")
        
        all_chunks.extend(chunks)

        # transform the chunks into embeddings
        embeddings = []
        for chunk in all_chunks:
            embedding = self.embedding_model.embed_documents(chunk)
            embeddings.extend(embedding)
        print("Chunks into embedding transformation done!")

        # convert embedding list to numpy array as the input for faiss
        embeddings_np = np.array(embeddings)
        # get the dimension for embedding
        dimension = embeddings_np.shape[1]
        # use cosin similarity to create faiss index
        index = faiss.IndexFlatIP(dimension)
        # add all the embedding index into faiss
        index.add(embeddings_np)
        print("Index process done.")
        return index, all_chunks


    def retrieval(self, index, chunks):
        """
        Process： transform user query into embedding, search top k chunks from vector store like Faiss

        :param    index:   vector index store
        :param    chunks:  all chunks from document text
        :return   the most top k similarity chunks
        """
        # transform user query into embedding
        query_embedding = self.embedding_model.embed_query(self.user_query)
        # convert query embedding to numpy array as the input of Faiss
        query_embedding = np.array([query_embedding])
        # searching the top k similar results from Faiss store
        # return the top k similarity score and their indices in original chunks
        distances, indices = index.search(query_embedding, self.top_k)

        print(f"user query: {self.user_query}")
        print(f"the most {self.top_k} similar chunks:")

        results = []
        for i in range(self.top_k):
            # the most similar chunks
            result_chunk = chunks[indices[0][i]]
            # print(f"chunk {i}:\n{result_chunk}") 

            # the similarity socre of related chunks
            result_distance = distances[0][i]
            print(f"similarity score: {result_distance}\n")

            # save the related chunks
            results.append(result_chunk)

        print("retrieval process done.")
        return results
    

    def generation(self, chunks):
        """
        Process：   call LLM model API and get response
        
        :param      chunks: the related chunks with user query from index store
        :return:    the response from LLM model
        """

        # build context, format is "refer doc1: \n refer doc2: \n ..."
        context = ""
        for i, chunk in enumerate(chunks):
            context += f"refer doc{i+1}: \n{chunk}\n\n"

        # build final user prompt which include original user query and context
        prompt = f"{self.user_query}\n\n{context}"

        chatLLM = LLMClient(self.model, self.temperature)
        
        messages = [
            {"role": "system", "content": self.system},
            {"role": "user", "content": prompt}]
        print(f"prompt: \n{prompt}")
        response = chatLLM.invoke(messages)
        return response 


    def run(self):
        """
        Indexing -> Retrieval -> Generation
        
        :return:    the response from LLM model
        """
        index, all_chunks = self.indexing()
        related_chunks = self.retrieval(index, all_chunks)
        response = self.generation(related_chunks)
        return response