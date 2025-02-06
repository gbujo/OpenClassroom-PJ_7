# syntax=docker/dockerfile:1
FROM ubuntu:22.04

#GBUJ
WORKDIR sources/predict
COPY requierements.txt /

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install -r requierements.txt

# install app
COPY main.py model.pkl predict_client.py /

# final configuration
ENV FLASK_APP=main
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]