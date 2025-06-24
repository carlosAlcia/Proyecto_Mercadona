FROM python

WORKDIR /app

COPY requirements.txt .

RUN mkdir src

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

CMD ["python", "src/mcp_server_mercadona.py"]