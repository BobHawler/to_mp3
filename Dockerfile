FROM python:3.9

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg


COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]