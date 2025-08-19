FROM python:3.9-slim

WORKDIR /app
COPY mitm_proxy.py .

RUN pip install flask requests

EXPOSE 5001

CMD ["python", "mitm_proxy.py"]