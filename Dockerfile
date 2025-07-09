FROM python:3.12.7

LABEL maintainer="Alex Yang" version="1.0" app="genai rag demo"

WORKDIR  /var/app

COPY *.py .
COPY *.txt .
COPY config.yaml .
COPY start.bash .

EXPOSE 8501

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./start.bash

CMD ["start.bash"]