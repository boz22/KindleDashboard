FROM python:3.5.9
WORKDIR /usr/src/KindleDashboard
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "python", "app.py" ]
