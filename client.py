from utils import get_config_val
from langchain_openai import ChatOpenAI
import os

class LLMClient:
    def __init__(self, model:str, temperature:float):
        """
        Instace LLM Client with provided parameters
        api_key and base_url are the basic paramters that llm client need, 
        could config in the file: config.yaml or export to the envrionment
        
        :param      model: the choosed LLM Model
        :param      temperature: the choosed LLM Model
        :return:    ChatOpenAI client
        """
        self.model = model
        self.temperature = temperature
        config_api_key = get_config_val('api_key','model')
        config_base_url = get_config_val('base_url','model')
        self._api_key = config_api_key if config_api_key else os.getenv('api_key')
        self._base_url = config_base_url if config_base_url else os.getenv('base_url')
        self._client = self.llm_client()

    def llm_client(self):
        client = ChatOpenAI(
            api_key = self._api_key,
            base_url = self._base_url,
            model = self.model,  
            temperature = self.temperature
        )
        return client   

    def invoke(self, messages:list[object]):
        try:
            response = self._client.invoke(messages)
            print(f"LLM Response:\n{response}")
        except:
            print("Error! No response from LLM API.")
        return response.content if response else None

