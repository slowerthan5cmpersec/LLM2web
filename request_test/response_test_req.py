import requests

url = 'http://127.0.0.1:8000/generate/'
data = {'query' : '요즘 눈이 잘 안 보이는데 어떤 영양소가 부족한 걸까?'}

with requests.post(url, stream=True, json=data) as res:
    for line in res.iter_content(chunk_size=None):
        if line != ' ':
            print(line.decode('utf-8', errors="ignore"), flush=True)


