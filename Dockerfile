FROM python:3.9.19-slim

RUN apt update
RUN apt install -y ffmpeg
RUN apt install -y libopencv-dev
RUN apt install -y python3-opencv

RUN python3 -m pip install imutils
RUN python3 -m pip install numpy
RUN python3 -m pip install opencv-python

RUN ln -sf /bin/bash /bin/sh

COPY MotionDetect/ App/
WORKDIR /App
ENTRYPOINT ["tail", "-f", "/dev/null"]