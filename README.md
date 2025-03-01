# PillME

## before running
runpod / openAI / anthropic <- API 키 필요, [구글 독스](https://docs.google.com/document/d/1d9dwWi_1I1ka3cJxiVDRBJ3--9gN7M3svROZjlENnLw/edit?usp=drivesdk)에 요청
  

## **FastAPI** how to

### in terminal:

```terminal
uvicorn 파일이름:app --reload
# ex) vllm/main.py
uvicorn vllm/main:app --reload
```

### in powershell:

```powershell
FastAPI dev main.py
```


## Docker how to

### pre-setting
 * GPU 사용 가능해야 하기에 nvidia Docker Runtime image 설치 필요
 * [docker-nvidia/cuda](https://hub.docker.com/r/nvidia/cuda) tags에서 여러 버전 확인 가능
 * 서버 사양 맞춰서 

```Dockerfile
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
```
* 이부분 수정



### terminal

```terminal
docker build -t my-fastapi-app .
docker run --gpus all -p 8000:8000 my-fastapi-app
```

### after port generated
* 한번 직접 브라우저로 접속해서 **This site can’t be reached** 메시지
* 확인 후 다시 터미널 확인하면 모델 로딩 로그 확인 가능,
* 로딩 끝날때까지 기다리다가 포트 재생성되면 작업 시작

## request_test
* **.py**: 빠르게 모델 응답 & 스트리밍 여부 확인
* **.htm**: fetch & post + streaming + markdown 변환 예제 참고 (chatGPT 모방)
