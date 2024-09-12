import uvicorn
from fastapi import FastAPI
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
app = FastAPI()


@app.get("/")
async def root():

    roi ={
        # interval : period
       #   [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
        #   : ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        '1m' : '5d',
        '5m' : '5d',
        '15m' : '1mo',
        '30m' : '1mo',
        '60m' : '1y',
        '1d' : '1y'

    }
    for interval, period in roi.items():
        print(interval, period )
        # 애플 주식 데이터 가져오기
        data = yf.Ticker("NVDA")
        #['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        data = data.history(period=period, interval=interval)

        # data.index = data.index.tz_convert('Asia/Seoul')

        data['RSI'] = ta.RSI(data['Open'], timeperiod=14)

        # MACD 계산
        data['MACD'], data['MACD_signal'], data['MACD_hist'] = ta.MACD(data['Close'], fastperiod=12, slowperiod=26,
                                                                       signalperiod=9)

        # 볼린저 밴드 계산
        data['upperband'], data['middleband'], data['lowerband'] = ta.BBANDS(data['Close'], timeperiod=20, nbdevup=2,
                                                                             nbdevdn=2, matype=0)

        # DMI- (Directional Movement Index Minus) 계산
        data['DMI_minus'] = ta.MINUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)

        # 결과 출력
        # print(data[['Close', 'RSI', 'MACD', 'MACD_signal', 'upperband', 'middleband', 'lowerband']])

        # def check_rsi_macd(data):
        #     signals = []
        #
        #     for i in range(1, len(data)):
        #         # RSI가 30 미만인지 확인
        #         if data['RSI'].iloc[i] < 30:
        #             # MACD 히스토그램이 이전 값보다 상승했다가, 현재 값이 이전 값보다 큰지 확인
        #             if data['MACD_hist'].iloc[i - 1] > data['MACD_hist'].iloc[i]:
        #                 signals.append((data.index[i], "RSI < 30, MACD Histogram 감소"))
        #
        #     return signals
        #
        #
        # # 신호 체크
        # signals = check_rsi_macd(data)
        #
        # for signal in signals:
        #     print(f"Signal at {signal[0]}: {signal[1]}")


        # DMI-가 최고점이고, RSI가 최저점인지 확인하는 로직
        def check_dmi_rsi(data):
            signals = []

            for i in range(1, len(data) - 1):
                # DMI-가 이전 값보다 커졌다가 줄어드는 시점
                if data['DMI_minus'].iloc[i - 1] < data['DMI_minus'].iloc[i] and data['DMI_minus'].iloc[i] > \
                        data['DMI_minus'].iloc[i + 1]:
                    # RSI가 이전 값보다 작아졌다가 상승하는 시점 (RSI 최저점)
                    if data['RSI'].iloc[i - 1] > data['RSI'].iloc[i] and data['RSI'].iloc[i] < data['RSI'].iloc[i + 1]:
                        # 추가 조건: RSI가 30 미만이고, DMI-가 30 이상일 때
                        if data['RSI'].iloc[i] < 30 and data['DMI_minus'].iloc[i] > 30:
                            signals.append((data.index[i], "DMI- 최고점, RSI 최저점, RSI < 30, DMI- > 30"))

            return signals

        # 신호 체크
        signals = check_dmi_rsi(data)

        # 결과 출력
        for signal in signals:
            print(f"Signal at {signal[0]}: {signal[1]}")


        # 그래프 그리기
        plt.figure(figsize=(14, 8))

        # Close price plot
        plt.subplot(3, 1, 1)
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.plot(data.index, data['upperband'], label='Upper Band', linestyle='--')
        plt.plot(data.index, data['middleband'], label='Middle Band', linestyle='--')
        plt.plot(data.index, data['lowerband'], label='Lower Band', linestyle='--')
        plt.title('NVDA Close Price with Bollinger Bands')
        plt.legend()

        # RSI plot
        plt.subplot(3, 1, 2)
        plt.plot(data.index, data['RSI'], label='RSI', color='orange')
        plt.axhline(70, color='red', linestyle='--')
        plt.axhline(30, color='green', linestyle='--')
        plt.title('RSI')

        # MACD plot
        plt.subplot(3, 1, 3)
        plt.plot(data.index, data['MACD'], label='MACD', color='blue')
        plt.plot(data.index, data['MACD_signal'], label='Signal Line', color='red')
        plt.bar(data.index, data['MACD_hist'], label='MACD Histogram', color='red')
        plt.title('MACD')
        plt.legend()

        plt.tight_layout()
        plt.show()

    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
