FROM python:3.9-slim
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY ./data/ ./data/
COPY ./normal-exporter.py .
EXPOSE 8001
ENV path='data/normal_test_20211030.csv'
CMD ["python", "./normal-exporter.py"]
