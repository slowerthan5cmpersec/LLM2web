import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  #! CORS
from pydantic import BaseModel

from vllm import EngineArgs, LLMEngine, SamplingParams, AsyncEngineArgs, AsyncLLMEngine

import uuid


# LLM 엔진 초기 설정
engineargs = AsyncEngineArgs(
    model="models/",
    # dtype='half',
    # tensor_parallel_size=2
    quantization='fp8',     # experts_int8
    trust_remote_code=True,
    kv_cache_dtype='fp8',
    max_model_len=512,
    # cpu_offload_gb=20,        # makes it fuckin slow and really use DRAM
    gpu_memory_utilization=0.95,

)
llm = AsyncLLMEngine.from_engine_args(engineargs)

sampling_params = SamplingParams(temperature=0.5, top_p=0.7, repetition_penalty=1.1, max_tokens=1024)

example_input = {
    "prompt": "Answer to user's question asap",
    "stream": True, # assume the non-streaming case
    "temperature": 0.0,
    "request_id": 0,
}




# 서버 설정
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/generate")
async def generate_post(request: QueryRequest):
    
    request_id = str(uuid.uuid4())
    llm.add_request(request_id, request.query, sampling_params)
    sent_text = ""

    async def stream_response():
        nonlocal sent_text
        while True:
            request_outputs = llm.generate(example_input["prompt"],
                                           sampling_params,
                                           example_input["request_id"])


            async for output in request_outputs:
                # if output.request_id == request_id:
                text = output.outputs[0].text

                # 새 텍스트만 추출 (기존에 출력한 텍스트는 응답하지 않도록)
                new_text = text[len(sent_text):]
                sent_text = text

                yield new_text
                    
                if output.finished:
                    return
                    
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