# syntax=docker/dockerfile:1
FROM python:3.8.5
WORKDIR /app
RUN apt-get update
RUN git clone git://github.com/JohnnyEngineer/RealOptions.git
RUN pip3 install -r requirements.txt
RUN cd RealOptions
RUN python App.py
CMD [ "python3", "App.py"]


