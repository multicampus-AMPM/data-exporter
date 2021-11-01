FROM python:3.9-slim
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY ./data/ ./data/
COPY ./failure-exporter.py .
EXPOSE 8002
ENV path='data/failure_test_20211030.csv'
CMD ["python", "./failure-exporter.py"]
