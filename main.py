import uvicorn
from fastapi import FastAPI
import yfinance as yf
import matplotlib.pyplot as plt
from TADomain import TADomain

app = FastAPI()
taDomain = TADomain()

@app.get("/")
async def root():

    roi ={
        # interval : period
       #   [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
        #   : ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        # '1m' : '5d',
        # '5m' : '5d',
        # '15m' : '1mo',
        # '30m' : '1mo',
        # '60m' : '1y',
        '1d' : '1y'

    }
    for interval, period in roi.items():
        print(interval, period )
        # 애플 주식 데이터 가져오기
        data = yf.Ticker("NVDA")
        #['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        data = data.history(period=period, interval=interval)

        # data.index = data.index.tz_convert('Asia/Seoul')

        print(taDomain.setCandleShape(data))
        taDomain.setCandlePattern(data)
        # taDomain.isReverseArrange(data)
        # taDomain.ichimoku_cloud(data)



    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
