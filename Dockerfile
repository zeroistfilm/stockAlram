FROM python:3.10

RUN pip install uvicorn fastapi yfinance ta-lib numpy==1.26.4 matplotlib