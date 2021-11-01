FROM python:3.9-slim
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY ./data/ ./data/
COPY ./baidu-exporter.py .
EXPOSE 8000
ENV path='data/baidu_sample.csv'
CMD ["python", "./baidu-exporter.py"]
