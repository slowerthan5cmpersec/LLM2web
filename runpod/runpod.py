import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  #! CORS
from pydantic import BaseModel

import uuid
from openai import OpenAI


client = OpenAI(
    api_key='',
    base_url=f"",
)



# 서버 설정
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class QueryRequest(BaseModel):
    query: str


@app.post("/generate")
async def generate_post(request: QueryRequest):
  response_stream = client.chat.completions.create(
  model='fivecmpersec/PillME-POCO-v0-7.8B',
  messages=[
     {"role": "system", "content": "너는 필미가 만든 영양관리 전문 채팅 모델 포코야. \n사용자의 답변에 하나도 빠짐없이 자세히 답변해줘. \n마지막에 내용을 한줄로 잘 정리해주길 바래"}, 
     {"role": "user", "content": f"{request.query}"}
     ],
  temperature=0,
  max_tokens=400,
  stream=True)
  

  async def stream_response():
      for response in response_stream:
        print(response.choices[0].delta.content or "", end="", flush=True)
        yield response.choices[0].delta.content
                                                      
        await asyncio.sleep(0.1)

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
