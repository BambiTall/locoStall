FROM python:3.7.2-stretch

# 容器內執行 python 的路徑
WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt && \
    pip install python-dotenv && \
    pip install flask-cors && \
    pip install pymysql

# flask 主程式檔名是 __init__.py
ENV FLASK_APP=__init__.py

# 讓其他人都可以連入 flask
ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_ENV=development

COPY . /app

EXPOSE 5000

CMD ["flask", "run"]