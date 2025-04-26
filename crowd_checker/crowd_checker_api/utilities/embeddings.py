

from openai import OpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from abc import ABC, abstractmethod


class ModelEmbeddings(ABC):
    def __init__(self, model_name):
        self.model_name = model_name

    @abstractmethod
    def gen_embeddings(self, text: str):
        pass


class HuggingFaceModelEmbeddings(ModelEmbeddings):
    def __init__(self, model_name: str = "thenlper/gte-small"):
        super().__init__(model_name)
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.model_name)

    def gen_embeddings(self, text: str) -> list:
        return list(self.embedding_model.embed_query(text))


class OpenAIModelEmbeddings(ModelEmbeddings):
    def __init__(self, model_name: str = "text-embedding-3-small"):
        super().__init__(model_name)
        self.client = OpenAI()

    def gen_embeddings(self, text: str):
        response = self.client.embeddings.create(model=self.model_name,
        input=[text])
        return response.data[0].embedding








