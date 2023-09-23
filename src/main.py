import signal
from typing import Optional
import asyncio
from pydantic import BaseModel  
import uvicorn
from fastapi import FastAPI
import subprocess
from celery import Celery
import json
import time
from recaptcha_solver import RecaptchaSolver
from dotenv import load_dotenv
import os
from utils import get_enumproxy
load_dotenv()
app = FastAPI()
class info(BaseModel):
    pageurl: str
    sitekey: str
    # proxy: Optional[int]
BROKER = os.getenv('BROKER')
BACKEND = os.getenv('BACKEND')
celery_app = Celery(
    "main",
    broker=BROKER,
    backend=BACKEND
)


def captcha_solver(pageurl):
    #host, port = get_enumproxy()
    #proxies = {'host':host, 'port': port}
    rcs = RecaptchaSolver(pageurl, use_proxies=True)
    # time.sleep(1.5)
    return  rcs.solve()
        # return recaptcha_token
    # else:
    #     return False
    # pass



@celery_app.task
@app.post("/runserver/")
async def run_task(info: info):
    start_time = time.time()
    pageurl = info.pageurl
    result = captcha_solver(pageurl)
    end_time = time.time()
    elapsed_time = end_time - start_time
    # info = f"Elapsed Time: {elapsed_time}"
    return {"Response": result, "Elapsed Time": elapsed_time}
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    uvicorn.run(app="main:app")
    # subprocess.run(command)
