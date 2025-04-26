import os
import openai
from langchain.llms import OpenAI
from langchain_core.runnables import Runnable
from langchain.prompts import PromptTemplate




class LLMQuery:
    def __init__(self, template_query: str, variables: list):
        # should get key via secret
        self.template_query = template_query
        self.variables = variables


    def __setup_prompt(self) -> Runnable:
        prompt = PromptTemplate(
            template=self.template_query,
            input_variables=self.variables,
        )
        llm = OpenAI()
        return prompt | llm

    def query(self, input: dict):
        runnable = self.__setup_prompt()
        return runnable.invoke(input)
