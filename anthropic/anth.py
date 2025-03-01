import asyncio
from langchain_huggingface import HuggingFacePipeline
from langgraph.graph import END, StateGraph, START, MessagesState
from typing import Dict,TypedDict
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import torch
from transformers import pipeline, TextStreamer
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate #, SystemMessagePromptTemplate,  HumanMessagePromptTemplate


callbacks = [StreamingStdOutCallbackHandler()]



from langchain_anthropic import ChatAnthropic

# import uuid
import getpass
import os


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = ''   # getpass.getpass(f"{var}: ")

_set_env("ANTHROPIC_API_KEY")

llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")


# llm = HuggingFacePipeline.from_model_id(
#   model_id='beomi/EXAONE-3.5-2.4B-Instruct-Llamafied',
#   task='text-generation',

# )

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "유저의 질문에 잘 답변해주기를 바래"),
    ("user", "{input}"),
    ('assistant', '답변드리겠습니다.')
])


chain = chat_prompt | llm | StrOutputParser()


for chunk in chain.stream("where is seoul"):
  print(chunk)

# print('dd')
# print(chain.invoke('where is seoul'))