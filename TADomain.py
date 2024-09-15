
import talib as ta
import matplotlib.pyplot as plt

class TADomain:
    def __init__(self):
        pass

    def setCandleShape(self, data):

        # Candle Shape
        data['Body'] = data['Close'] - data['Open']
        data['UpperShadow'] = data['High'] - data[['Open', 'Close']].max(axis=1)
        data['LowerShadow'] = data[['Open', 'Close']].min(axis=1) - data['Low']

        # Candle Shape Ratio
        candle_range = data['High'] - data['Low']
        data['BodyRatio'] = abs(data['Body']) /candle_range
        data['UpperShadowRatio'] = data['UpperShadow'] /candle_range
        data['LowerShadowRatio'] = data['LowerShadow'] / candle_range

        # Candle Shape Type 초기화
        data['CandleShapeEn'] = 'None'
        data['CandleShapeKr'] = 'None'

        # 캔들 패턴 영어 버전
        patterns_en = {
            'Long Bearish Candle': 'Long Bearish Candle',
            'Long Bullish Candle': 'Long Bullish Candle',
            'Upper Shadow Bullish': 'Upper Shadow Bullish',
            'Upper Shadow Bearish': 'Upper Shadow Bearish',
            'Lower Shadow Bullish': 'Lower Shadow Bullish',
            'Lower Shadow Bearish': 'Lower Shadow Bearish',
            'Both Shadow Bullish': 'Both Shadow Bullish',
            'Both Shadow Bearish': 'Both Shadow Bearish',
            'Doji Bullish': 'Doji Bullish',
            'Doji Bearish': 'Doji Bearish',
            'Dragonfly Doji': 'Dragonfly Doji',
            'Gravestone Doji': 'Gravestone Doji',
            'Bullish Candle': 'Bullish Candle',
            'Bearish Candle': 'Bearish Candle'
        }

        # 캔들 패턴 한글 버전
        patterns_kr = {
            'Long Bearish Candle': '장대 음봉',
            'Long Bullish Candle': '장대 양봉',
            'Upper Shadow Bullish': '위꼬리 양봉',
            'Upper Shadow Bearish': '위꼬리 음봉',
            'Lower Shadow Bullish': '아래꼬리 양봉',
            'Lower Shadow Bearish': '아래꼬리 음봉',
            'Both Shadow Bullish': '양꼬리 양봉',
            'Both Shadow Bearish': '양꼬리 음봉',
            'Doji Bullish': '십자 도지 (상승)',
            'Doji Bearish': '십자 도지 (하락)',
            'Dragonfly Doji': '잠자리형 도지',
            'Gravestone Doji': '비석형 도지',
            'Bullish Candle': '양봉',
            'Bearish Candle': '음봉'
        }

        # 장대 음봉: 긴 몸통 음봉
        data.loc[(data['BodyRatio'] > 0.7) & (data['Body'] < 0), ['CandleShapeEn', 'CandleShapeKr']] = [
            patterns_en['Long Bearish Candle'], patterns_kr['Long Bearish Candle']]

        # 장대 양봉: 긴 몸통 양봉
        data.loc[(data['BodyRatio'] > 0.7) & (data['Body'] > 0), ['CandleShapeEn', 'CandleShapeKr']] = [
            patterns_en['Long Bullish Candle'], patterns_kr['Long Bullish Candle']]

        # 위꼬리 양봉
        data.loc[
            (data['Body'] > 0) & (data['UpperShadowRatio'] >= 0.3) & (data['LowerShadowRatio'] < 0.2), ['CandleShapeEn',
                                                                                                        'CandleShapeKr']] = [
            patterns_en['Upper Shadow Bullish'], patterns_kr['Upper Shadow Bullish']]

        # 위꼬리 음봉
        data.loc[
            (data['Body'] < 0) & (data['UpperShadowRatio'] >= 0.3) & (data['LowerShadowRatio'] < 0.2), ['CandleShapeEn',
                                                                                                        'CandleShapeKr']] = [
            patterns_en['Upper Shadow Bearish'], patterns_kr['Upper Shadow Bearish']]

        # 아래꼬리 양봉
        data.loc[
            (data['Body'] > 0) & (data['LowerShadowRatio'] >= 0.3) & (data['UpperShadowRatio'] < 0.2), ['CandleShapeEn',
                                                                                                        'CandleShapeKr']] = [
            patterns_en['Lower Shadow Bullish'], patterns_kr['Lower Shadow Bullish']]

        # 아래꼬리 음봉
        data.loc[
            (data['Body'] < 0) & (data['LowerShadowRatio'] >= 0.3) & (data['UpperShadowRatio'] < 0.2), ['CandleShapeEn',
                                                                                                        'CandleShapeKr']] = [
            patterns_en['Lower Shadow Bearish'], patterns_kr['Lower Shadow Bearish']]

        # 양꼬리 양봉
        data.loc[(data['Body'] > 0) & (data['UpperShadowRatio'] >= 0.3) & (data['LowerShadowRatio'] >= 0.3), [
            'CandleShapeEn', 'CandleShapeKr']] = [patterns_en['Both Shadow Bullish'],
                                                  patterns_kr['Both Shadow Bullish']]

        # 양꼬리 음봉
        data.loc[(data['Body'] < 0) & (data['UpperShadowRatio'] >= 0.3) & (data['LowerShadowRatio'] >= 0.3), [
            'CandleShapeEn', 'CandleShapeKr']] = [patterns_en['Both Shadow Bearish'],
                                                  patterns_kr['Both Shadow Bearish']]

        # 십자 도지 (상승)
        data.loc[(abs(data['Body']) < 0.05 * candle_range) & (data['Close'] > data['Open']), ['CandleShapeEn',
                                                                                              'CandleShapeKr']] = [
            patterns_en['Doji Bullish'], patterns_kr['Doji Bullish']]

        # 십자 도지 (하락)
        data.loc[(abs(data['Body']) < 0.05 * candle_range) & (data['Close'] < data['Open']), ['CandleShapeEn',
                                                                                              'CandleShapeKr']] = [
            patterns_en['Doji Bearish'], patterns_kr['Doji Bearish']]

        # 잠자리형 도지 (아래꼬리만 긴 도지)
        data.loc[(abs(data['Body']) < 0.05 * candle_range) & (data['LowerShadowRatio'] >= 0.3) & (
                    data['UpperShadowRatio'] < 0.1), ['CandleShapeEn', 'CandleShapeKr']] = [
            patterns_en['Dragonfly Doji'], patterns_kr['Dragonfly Doji']]

        # 비석형 도지 (위꼬리만 긴 도지)
        data.loc[(abs(data['Body']) < 0.05 * candle_range) & (data['UpperShadowRatio'] >= 0.3) & (
                    data['LowerShadowRatio'] < 0.1), ['CandleShapeEn', 'CandleShapeKr']] = [
            patterns_en['Gravestone Doji'], patterns_kr['Gravestone Doji']]

        # 일반 양봉
        data.loc[(data['CandleShapeEn'] == 'None') & (data['Body'] > 0), ['CandleShapeEn', 'CandleShapeKr']] = [
            patterns_en['Bullish Candle'], patterns_kr['Bullish Candle']]

        # 일반 음봉
        data.loc[(data['CandleShapeEn'] == 'None') & (data['Body'] < 0), ['CandleShapeEn', 'CandleShapeKr']] = [
            patterns_en['Bearish Candle'], patterns_kr['Bearish Candle']]

        return data

    def setCandlePattern(self, data):
        data['PatternEn'] = 'None'
        data['PatternKr'] = 'None'

        # 1. 상승 장악형 (Bullish Engulfing Pattern)
        data.loc[(data['Close'].shift(1) < data['Open'].shift(1)) &  # 첫 번째 캔들 음봉
                 (data['Close'] > data['Open']) &  # 두 번째 캔들 양봉
                 (data['Close'] > data['Open'].shift(1)) &  # 두 번째 캔들 종가가 첫 번째 캔들 시가보다 높음
                 (data['Open'] < data['Close'].shift(1)),  # 두 번째 캔들 시가가 첫 번째 캔들 종가보다 낮음
        ['PatternEn', 'PatternKr']] = ['Bullish Engulfing', '상승 장악형']

        # 2. 적삼병 (Three White Soldiers)
        data.loc[(data['Close'] > data['Open']) &  # 첫 번째 양봉
                 (data['Close'].shift(1) > data['Open'].shift(1)) &  # 두 번째 양봉
                 (data['Close'].shift(2) > data['Open'].shift(2)) &  # 세 번째 양봉
                 (data['Close'] > data['Close'].shift(1)) &  # 현재 종가가 전일 종가보다 높음
                 (data['Close'].shift(1) > data['Close'].shift(2)),  # 전일 종가가 그 전날보다 높음
        ['PatternEn', 'PatternKr']] = ['Three White Soldiers', '적삼병']

        # 3. 흑삼병 (Three Black Crows)
        data.loc[(data['Close'] < data['Open']) &  # 첫 번째 음봉
                 (data['Close'].shift(1) < data['Open'].shift(1)) &  # 두 번째 음봉
                 (data['Close'].shift(2) < data['Open'].shift(2)) &  # 세 번째 음봉
                 (data['Close'] < data['Close'].shift(1)) &  # 현재 종가가 전일 종가보다 낮음
                 (data['Close'].shift(1) < data['Close'].shift(2)),  # 전일 종가가 그 전날보다 낮음
        ['PatternEn', 'PatternKr']] = ['Three Black Crows', '흑삼병']

        # 4. 셋별형 (Morning Star) - 상승 신호
        data.loc[(data['Close'].shift(2) < data['Open'].shift(2)) &  # 첫 번째 음봉
                 (data['Close'].shift(1) < data['Open'].shift(1)) &  # 두 번째 캔들 작은 몸통
                 (data['Close'] > data['Open']) &  # 세 번째 양봉
                 (data['Open'].shift(1) > data['Close'].shift(2)) &  # 두 번째 캔들의 시가가 첫 번째 음봉의 종가보다 낮음 (갭 발생)
                 (data['Open'] < data['Close'].shift(1)),  # 세 번째 캔들의 시가가 두 번째 캔들의 종가보다 낮음
        ['PatternEn', 'PatternKr']] = ['Morning Star', '셋별형 상승']

        # 5. 석별형 (Evening Star) - 하락 신호
        data.loc[(data['Close'].shift(2) > data['Open'].shift(2)) &  # 첫 번째 양봉
                 (data['Close'].shift(1) > data['Open'].shift(1)) &  # 두 번째 캔들 작은 몸통
                 (data['Close'] < data['Open']) &  # 세 번째 음봉
                 (data['Open'].shift(1) < data['Close'].shift(2)) &  # 두 번째 캔들의 시가가 첫 번째 양봉의 종가보다 높음 (갭 발생)
                 (data['Open'] > data['Close'].shift(1)),  # 세 번째 캔들의 시가가 두 번째 캔들의 종가보다 높음
        ['PatternEn', 'PatternKr']] = ['Evening Star', '석별형 하락']

        # 6. 상승세 신호 캔들 (Rising Window)
        data.loc[(data['Open'] > data['Close'].shift(1)) &  # 금일 시가가 전일 종가보다 높음
                 (data['Close'] > data['Open']) &  # 금일 양봉
                 (data['Open'] > data['High'].shift(1)),  # 금일 시가가 전일 최고가보다 높음 (갭 발생)
        ['PatternEn', 'PatternKr']] = ['Rising Window', '상승세 신호 캔들']

        # 7. 하락세 신호 캔들 (Falling Window)
        data.loc[(data['Open'] < data['Close'].shift(1)) &  # 금aaa일 시가가 전일 종가보다 낮음
                 (data['Close'] < data['Open']) &  # 금일 음봉
                 (data['Open'] < data['Low'].shift(1)),  # 금일 시가가 전일 최저가보다 낮음 (갭 발생)
        ['PatternEn', 'PatternKr']] = ['Falling Window', '하락세 신호 캔들']

        # 8. 잉태형 (Inside Bar) - 상승 반전 신호
        data.loc[(data['Close'].shift(1) < data['Open'].shift(1)) &  # 첫 번째 음봉
                 (data['Close'] > data['Open']) &  # 두 번째 양봉
                 (data['Close'] < data['Open'].shift(1)) &  # 두 번째 양봉이 첫 번째 음봉 시가보다 낮음
                 (data['Open'] > data['Close'].shift(1)),  # 두 번째 양봉 시가가 첫 번째 음봉 종가보다 높음
        ['PatternEn', 'PatternKr']] = ['Bullish Inside Bar', '잉태형 상승']


        for i in range(len(data)):
            if data['PatternEn'].iloc[i] != 'None':
                print(f"{data.index[i]}: {data['PatternKr'].iloc[i]}")
        return data

    def isReverseArrange(self, data):
        MA5 = ta.MA(data['Close'], timeperiod=5, matype=0)
        MA20 = ta.MA(data['Close'], timeperiod=20, matype=0)
        MA30 = ta.MA(data['Close'], timeperiod=30, matype=0)
        MA60 = ta.MA(data['Close'], timeperiod=60, matype=0)
        MA120 = ta.MA(data['Close'], timeperiod=120, matype=0)


        reverseArrange = MA5.iloc[-1] < MA20.iloc[-1] < MA30.iloc[-1] < MA60.iloc[-1] < MA120.iloc[-1]
        crossed20_only = MA20.iloc[-1] < MA5.iloc[-1] < MA30.iloc[-1] < MA60.iloc[-1] < MA120.iloc[-1]
        crossed30_only = MA20.iloc[-1] < MA30.iloc[-1] < MA5.iloc[-1] < MA60.iloc[-1] < MA120.iloc[-1]
        crossed60_only = MA20.iloc[-1] < MA30.iloc[-1] < MA60.iloc[-1] < MA5.iloc[-1] < MA120.iloc[-1]
        crossed120_only = MA20.iloc[-1] < MA30.iloc[-1] < MA60.iloc[-1] < MA120.iloc[-1] < MA5.iloc[-1]

        print("isReverseArrange: ", reverseArrange)
        print("crossed20_only: ", crossed20_only)
        print("crossed30_only: ", crossed30_only)
        print("crossed60_only: ", crossed60_only)
        print("crossed120_only: ", crossed120_only)

    def ichimoku_cloud(self, data):
        # 전환선(Tenkan-sen): (9일 중 최고가 + 9일 중 최저가) / 2
        nine_period_high = ta.MAX(data['High'], timeperiod=9)
        nine_period_low = ta.MIN(data['Low'], timeperiod=9)
        tenkan_sen = (nine_period_high + nine_period_low) / 2

        # 기준선(Kijun-sen): (26일 중 최고가 + 26일 중 최저가) / 2
        twenty_six_period_high = ta.MAX(data['High'], timeperiod=26)
        twenty_six_period_low = ta.MIN(data['Low'], timeperiod=26)
        kijun_sen = (twenty_six_period_high + twenty_six_period_low) / 2

        # 선행스팬 1(Senkou Span A): (전환선 + 기준선) / 2, 26일 앞
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

        # 선행스팬 2(Senkou Span B): (52일 중 최고가 + 52일 중 최저가) / 2, 26일 앞
        fifty_two_period_high = ta.MAX(data['High'], timeperiod=52)
        fifty_two_period_low = ta.MIN(data['Low'], timeperiod=52)
        senkou_span_b = ((fifty_two_period_high + fifty_two_period_low) / 2).shift(26)

        # 후행스팬(Chikou Span): 종가를 26일 뒤로 이동
        chikou_span = data['Close'].shift(-26)

        # DataFrame에 각 지표 추가
        data['Tenkan-sen'] = tenkan_sen
        data['Kijun-sen'] = kijun_sen
        data['Senkou Span A'] = senkou_span_a
        data['Senkou Span B'] = senkou_span_b
        data['Chikou Span'] = chikou_span

        plt.figure(figsize=(14, 7))

        # 종가 (Close)
        plt.plot(data['Close'], label='Close', color='black', linewidth=1.5)

        # 전환선 (Tenkan-sen)
        plt.plot(data['Tenkan-sen'], label='Tenkan-sen', color='blue', linestyle='--')

        # 기준선 (Kijun-sen)
        plt.plot(data['Kijun-sen'], label='Kijun-sen', color='red', linestyle='--')

        # 양운 (Senkou Span A > Senkou Span B)
        plt.fill_between(data.index, data['Senkou Span A'], data['Senkou Span B'],
                         where=(data['Senkou Span A'] > data['Senkou Span B']),
                         color='red', alpha=0.5, label='양운 (Positive Cloud)')

        # 음운 (Senkou Span A < Senkou Span B)
        plt.fill_between(data.index, data['Senkou Span A'], data['Senkou Span B'],
                         where=(data['Senkou Span A'] < data['Senkou Span B']),
                         color='blue', alpha=0.5, label='음운 (Negative Cloud)')

        # 후행스팬 (Chikou Span)
        plt.plot(data['Chikou Span'], label='Chikou Span', color='green')

        # 제목 및 범례 추가
        plt.title('Ichimoku Kinko Hyo (일목균형표)')
        plt.legend(loc='best')
        plt.grid(True)
        plt.show()

        return data




    def check_rsi_macd(self,data):
        data['RSI'] = ta.RSI(data['Open'], timeperiod=14)
        data['MACD'], data['MACD_signal'], data['MACD_hist'] = ta.MACD(data['Close'], fastperiod=12, slowperiod=26,
                                                                       signalperiod=9)
        data['upperband'], data['middleband'], data['lowerband'] = ta.BBANDS(data['Close'], timeperiod=20, nbdevup=2,
                                                                             nbdevdn=2, matype=0)
        data['DMI_minus'] = ta.MINUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)

        signals = []

        for i in range(1, len(data)):
            # RSI가 30 미만인지 확인
            if data['RSI'].iloc[i] < 30:
                # MACD 히스토그램이 이전 값보다 상승했다가, 현재 값이 이전 값보다 큰지 확인
                if data['MACD_hist'].iloc[i - 1] > data['MACD_hist'].iloc[i]:
                    signals.append((data.index[i], "RSI < 30, MACD Histogram 감소"))

        for signal in signals:
            print(f"Signal at {signal[0]}: {signal[1]}")


        return signals


    def check_dmi_rsi(self, data):

        data['RSI'] = ta.RSI(data['Open'], timeperiod=14)
        data['MACD'], data['MACD_signal'], data['MACD_hist'] = ta.MACD(data['Close'], fastperiod=12, slowperiod=26,
                                                                       signalperiod=9)
        data['upperband'], data['middleband'], data['lowerband'] = ta.BBANDS(data['Close'], timeperiod=20, nbdevup=2,
                                                                             nbdevdn=2, matype=0)

        data['DMI_minus'] = ta.MINUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)

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


        for signal in signals:
            print(f"Signal at {signal[0]}: {signal[1]}")

        return signals

