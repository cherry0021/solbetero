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
app = FastAPI()
class info(BaseModel):
    pageurl: str
    sitekey: str
    # proxy: Optional[int]
celery_app = Celery(
    "main",
    broker="redis://default:a5hbNOjYd31fw0lWCUM2@containers-us-west-107.railway.app:7431",
    backend="redis://default:U2O31SnSLTTXGpz95eo5@containers-us-west-97.railway.app:6855"
)


def captcha_solver(pageurl):
    rcs = RecaptchaSolver(pageurl)
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
    
    uvicorn.run(app="main:app", port=8800, host='0.0.0.0', workers=10, limit_max_requests=50, timeout_graceful_shutdown=420)
    # subprocess.run(command)