FROM python:3.12

RUN apt-get update && apt-get install -y locales

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# comment the line below
# and uncomment the line after
# if you wish to run in prod mode
RUN chmod +x watcher-docker 
# CMD ["python", "main.py"]
