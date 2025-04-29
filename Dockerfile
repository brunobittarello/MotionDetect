FROM python:3.9.19

RUN apt update
RUN apt install -y ffmpeg
RUN apt install -y libopencv-dev
RUN apt install -y python3-opencv

RUN python3 -m pip install imutils
RUN python3 -m pip install numpy
RUN python3 -m pip install opencv-python

# FROM python:3.13-slim
# FROM hdgigante/python-opencv:4.9.0-ubuntu

# RUN apt-get update
# RUN apt-get install -y iputils-ping
# RUN apt-get install -y ffmpeg
# RUN apt-get install -y libopencv-dev

# RUN apt-get install -y v4l-utils
# RUN apt-get install -y python3-opencv

# RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
# RUN tar xvf ffmpeg-git-amd64-static.tar.xz
# RUN echo $PATH /usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:/home/john/.local/bin:/home/john/bin


# Ping function
# pip install --upgrade pip
# RUN python3 -m pip install imutils
# RUN python3 -m pip install numpy
# RUN python3 -m pip install opencv-python==4.10.0.82

# RUN python3 -m pip install onvif-zeep
# RUN python3 -m pip install pyptz

RUN ln -sf /bin/bash /bin/sh

COPY MotionDetect/ App/
WORKDIR /App
ENTRYPOINT ["tail", "-f", "/dev/null"]