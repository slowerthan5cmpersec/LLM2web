# PillME

## before running
~~put all model files to **models**~~
  
~~can do it in once by **model_dohwnload.py** (for test)~~
  
  
  
## nothing done(dk how to do):

- ~~**Dockerfile**~~ (works well? (cant use local model file, so slow on loading + some bugs))

- **SQL** (for conversation data saving)



  
  
## **FastAPI** how to load api server

### in terminal:

```
uvicorn main:app --reload
```

### in powershell:

```
FastAPI dev main.py
```
  
  
## **server** at least

- vram > 16GB, as possible solitary GPU (if more than 2, not efficient + refactoring code)

- dram > 40GB

- ~~SSD > os.path.getsize(models)~~ (cant use local model file temporarily, so dont care)
