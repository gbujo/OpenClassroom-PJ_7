# syntax=docker/dockerfile:1
FROM ubuntu:22.04

#GBUJ
#WORKDIR /sources/predict
COPY /sources/predict/requierements.txt /

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install -r requierements.txt

# install app
COPY /sources/predict/main.py /sources/predict/model.pkl /sources/predict/predict_client.py /

# final configuration
ENV FLASK_APP=main
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]