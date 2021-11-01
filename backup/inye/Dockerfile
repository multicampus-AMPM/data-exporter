FROM python:3.9-slim
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY ./data/ ./data/
COPY ./test-exporter.py .
EXPOSE 8010
ENV path='data/test_test_mix.csv'
CMD ["python", "./test-exporter.py"]
