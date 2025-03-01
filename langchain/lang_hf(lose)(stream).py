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

model_path = 'models/'    # '/content/drive/MyDrive/PillME/beomi_EXAONE-3.5-7.8B-Instruct-Llamafied'

tokenizer = AutoTokenizer.from_pretrained(
    pretrained_model_name_or_path=model_path,
    device_map='cuda:0',
    max_length=1024,
    padding='max_length',
    truncation=True,
    batched=True
    )

bnbconfig = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_use_double_quant=True,
    bnb_8bit_quant_type='fp8',
    bnb_8bit_compute_dtype=torch.bfloat16
    # llm_int8_skip_modules=['lm_head', 'embed_tokens', 'mlp']
    )

model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=model_path,
    quantization_config=bnbconfig,
    # attn_implementation="flash_attention_2",
    trust_remote_code=True,
    # load_in_8bit=True,
    device_map='cuda:0')

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=128)  # , device='auto'
llm = HuggingFacePipeline(pipeline=pipe)

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