# syntax=docker/dockerfile:1
FROM python:3.8.5
MAINTAINER "Williamson Brigido"

RUN pip install pandas==1.1.3
RUN pip install numpy==1.19.2
RUN pip install matplotlib==3.3.2
RUN pip install networkx==2.5
RUN pip install scipy==1.5.2
RUN git clone git://github.com/JohnnyEngineer/RealOptions.git
WORKDIR RealOptions
CMD ["RealOptions/App.py"]
ENTRYPOINT ["python3"]
