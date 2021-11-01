FROM python:3.9-slim
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY ./collectd-alt-exporter.py .
EXPOSE 9103
CMD ["python", "./collectd-alt-exporter.py"]
