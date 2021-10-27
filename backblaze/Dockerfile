FROM python:3.9-slim
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY ./data/ ./data/
COPY ./backblaze-exporter.py .
EXPOSE 8002
ENV path='data/backblaze_2021_q2.csv'
CMD ["python", "./backblaze-exporter.py"]
