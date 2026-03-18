FROM python:3.11-slim

RUN pip install --no-cache-dir numpy scipy matplotlib pandas

WORKDIR /app

CMD ["python3", "-c", "import scipy; print('scipy', scipy.__version__)"]
