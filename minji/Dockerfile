FROM python:3.9-slim
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY ./data/ ./data/
COPY ./test-exporter.py .
EXPOSE 8008
ENV path='data/cd_iy.csv'
CMD ["python", "./test-exporter.py"]
