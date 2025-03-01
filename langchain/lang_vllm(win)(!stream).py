import asyncio
from fastapi import FastAPI#, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  #! CORS
from pydantic import BaseModel

import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
# from transformers import pipeline, TextStreamer

from langchain_core.prompts import ChatPromptTemplate #, SystemMessagePromptTemplate,  HumanMessagePromptTemplate
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import VLLM
# from langchain.memory import ConversationBufferWindowMemory
# from langchain.chains import LLMChain
# from langchain.llms import HuggingFacePipeline
# from langchain_core.messages import HumanMessage, SystemMessage
# from vllm.lora.request import LoRARequest
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
# from langchain.callbacks import stre

import uuid
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEndpoint




llm = VLLM(model="models/",
           trust_remote_code=True,  # mandatory for hf models
           max_new_tokens=1024,
           max_model_len=1024,
           max_seq_len=1024,
          #  streaming=True,
           stream=True,
          #  use_nvram=True,
          #  dtype='fp8', 
           vllm_kwargs={"quantization": "fp8"},
           temperature=0,
           gpu_memory_utilization=0.95,
          #  streaming_async=True,
          #  callbacks=[StreamingStdOutCallbackHandler()]
        #    tensor_parallel_size=4, # <- for multiple GPUs
           )

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "유저의 질문에 잘 답변해주기를 바래"),
    ("user", "{input}"),
    ('assistant', '답변드리겠습니다.')
])


chain = chat_prompt | llm | StrOutputParser()




for chunk in chain.stream('where is dragon?', callbacks=StreamingStdOutCallbackHandler()):
  print(chunk, flush=True)

# print(chain.invoke('where is seoul'))

# async def aa():
#   async for chunk in chain.astream('where is dragon?', callbacks=StreamingStdOutCallbackHandler()):
#     print(chunk)
