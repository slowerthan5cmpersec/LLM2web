import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  #! CORS
from pydantic import BaseModel

from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate #, SystemMessagePromptTemplate,  HumanMessagePromptTemplate
from langchain.callbacks import AsyncIteratorCallbackHandler

# import uuid
import getpass
import os


gpt_api_key = ''

stream_it = AsyncIteratorCallbackHandler()

llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo-16k",
                     openai_api_key=gpt_api_key, streaming=True,
                     callbacks=[stream_it],
                     )

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "유저의 질문에 잘 답변해주기를 바래. 마크다운 문법으로 답변을 구성하면 좋겠어!!"),
    ("user", "{input}"),
    ('assistant', '답변드리겠습니다.')
])


chain = chat_prompt | llm | StrOutputParser()




# 서버 설정
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class QueryRequest(BaseModel):
    query: str

@app.post("/generate")
async def generate_post(request: QueryRequest):
    sent_text = ""

    async def stream_response():
        nonlocal sent_text
            
        async for chunk in chain.astream(request.query, stream_mode=['custom']):
            # if chunk:     # .content
            yield chunk
                
                # 띄어쓰기 단위로 새로운 텍스트를 yield
                # for word in new_text.split(" "):
                    # if word:  # 빈 문자열 제외
                        # yield word      # + " "
                        # await asyncio.sleep(0.5)
                
                # 요청이 완료되면 종료
                # if output.finished:
                #     return
                
        await asyncio.sleep(0.001)

    return StreamingResponse(stream_response(), media_type="text/event-stream")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


origins = [
    "http://localhost.PillME.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.pillme.co.kr/",
    "http://127.0.0.1:3000/shobu.html"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# python -m uvicorn antman:app --reload