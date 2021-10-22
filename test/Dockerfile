FROM python:3.9-slim
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY ./data/ ./data/
COPY ./test-exporter.py .
EXPOSE 8001
ENV path='data/smart_test.csv'
CMD ["python", "./test-exporter.py"]
