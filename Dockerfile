FROM python:3.9

WORKDIR /covenant-finance-docker

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
