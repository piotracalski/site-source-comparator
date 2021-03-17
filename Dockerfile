FROM python:3.8

WORKDIR /compare-the-page

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "./main.py"]