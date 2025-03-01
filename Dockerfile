# Base image
# FROM python:3.12.7

# Install pytorch
# RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
RUN apt update && apt install -y python3-pip

# Set working directory
WORKDIR /fastapi


# Install python lib
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY ./models/* /fastapi/models
COPY ./main.py /fastapi/
# COPY ./packages /fastapi/packages


# CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8088"]
# or 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



# docker build -t myimage .
# docker run -d --name mycontainer -p 8000:8000 myimage
# docker rm / rmi ... -f
# docker images / docker ps

# docker run -it my-fastapi-app /bin/bash  # 컨테이너 내부로 들어감
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# final -> 
# docker build -t my-fastapi-app .
# docker run --gpus all -p 8000:8000 my-fastapi-app
# request "/", then model tensors will be loaded, wait, then done