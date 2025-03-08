# LLM2web


## before running
- **openAI** / **anthropic** / **huggingface** <- <ins>API</ins> 키 필요, [구글 독스](https://docs.google.com/document/d/1d9dwWi_1I1ka3cJxiVDRBJ3--9gN7M3svROZjlENnLw/edit?usp=drivesdk)에 요청
- **runpod** <- API + <ins>base_URL</ins> 필요, // 

## **FastAPI** how to

### in terminal:

```terminal
uvicorn 파일이름:app --reload
```
###### ex) vllm/main.py
```
uvicorn vllm/main:app --reload
```

### in powershell:

```powershell
FastAPI dev main.py
```


## Docker how to


### pre-setting


#### server with GPU
 * GPU 사용 가능해야 하기에 nvidia Docker Runtime image 설치 필요
 * [docker-nvidia/cuda](https://hub.docker.com/r/nvidia/cuda) tags에서 여러 버전 확인 가능
 * 서버 사양 맞춰서 
https://github.com/slowerthan5cmpersec/LLM2web/blob/69f88e1ddec6384b359bd88ab3625eea62f2b35d/Dockerfiles/Dockerfile#L7
* 이부분 수정
* [CUDA wiki](https://en.m.wikipedia.org/wiki/CUDA) GPUs supported 항목 참조






#### server with GPU_less (API)
* [Dockerfile_serverless](https://github.com/slowerthan5cmpersec/LLM2web/blob/main/Dockerfiles/Dockerfile_serverless) 사용
* 위 파일 Dockerfiles에서 최상위로 빼내고, 이름 Dockerfile로 바꾸고 사용
* 사용하려는 API 따라서
###### ex) openAI
https://github.com/slowerthan5cmpersec/LLM2web/blob/a4c15709129573fba688f2ab110dfbfd1f1ff21d/Dockerfiles/Dockerfile_serverless#L20
```Dockerfile
COPY ./openAI/open_main.py /fastapi/
```

https://github.com/slowerthan5cmpersec/LLM2web/blob/d634dae4f6e0b01e37dcd5bc4813ae7bb8e4f012/Dockerfiles/Dockerfile_serverless#L26
```Dockerfile
CMD ["uvicorn", "open_main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```
* 이런식으로 수정
* 사용 메인 파일에서 <ins>API key</ins>, <ins>base url</ins> 값 다 넣었는지 확인










### terminal
#### server with GPU
```terminal
docker build -t my-fastapi-app .
docker run --gpus all -p 8000:8000 my-fastapi-app
```
#### server with GPU_less (API)
```terminal
docker build -t my-fastapi-app .
docker run -d --name mycontainer -p 8000:8000 my-fastapi-app
```

### after port generated
#### server with GPU
* 한번 직접 브라우저로 접속해서 **This site can’t be reached** 메시지
* 확인 후 다시 터미널 확인하면 모델 로딩 로그 확인 가능,
* 로딩 끝날때까지 기다리다가 포트 재생성되면 작업 시작

## request_test
* **.py**: 빠르게 모델 응답 & 스트리밍 여부 확인
* **.htm**: fetch & post + streaming + markdown 변환 예제 참고 (chatGPT 모방)


## 구분

#### server with GPU
- langchain/vllm, **vllm**
#### server with GPU_less (API)
- langchain/hf, anthropic, **openAI**, **runpod**




## thinks

- runpod 직접 대여 <- rtx L4 <- |on demand 0.43$/hr| or |spot(interruptible) 0.22$/hr|
- 0.22$/h * 12h/d * 30d = 79.2(=80)$, interruptible이 뭔지 아직 경험 X
- dockerfile template 통해서 pod 생성 가능, 개발 일단 편해짐 (리눅스 ssh 대비)
- 토큰 바로바로 나옴, 속도 빠름
- prob: stop runpodctl pod id <- works / start runpodctl pod id <- spot방식이라고 못하게함, 웹 들어가서 직접 켜야함
- hence: 상남자 <- 아침 12시 밤 12시에 직접 키고 직접 끄기 / 귀찮아 <- 셀레니움으로 자동화하기(위험?할것같음)
- 우려: 가끔 수요 꽉찼다고 특정 gpu 못들어가게 하는 케이스 있음, 그게 L4라면 / 너무 작을수도 (request 한번에 gpu util 60% 뜸, async는 돼서 터질일은 없을듯)

### or
- serverless에서 active worker를 하나 지정
- 0.00010$/s 측정, 0.00010$/s * 3600s/h * 12h/d * 30d = 129.6$ (0.36$/h <-> 0.22$/h)
- 장점: 관리가 편할 것? / dis: expensive
- 30% discount 해준다는데 잘 모르겠음
