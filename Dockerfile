FROM python:3.13-slim

RUN apt-get update
RUN apt-get install -y iputils-ping
RUN apt-get install -y ffmpeg
# RUN apt-get install -y libopencv-dev
RUN apt-get install -y python3-opencv

# RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
# RUN tar xvf ffmpeg-git-amd64-static.tar.xz
# RUN echo $PATH /usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:/home/john/.local/bin:/home/john/bin


# Ping function

RUN python3 -m pip install imutils
RUN python3 -m pip install numpy
RUN python3 -m pip install opencv-python
# RUN python3 -m pip install onvif-zeep
# RUN python3 -m pip install pyptz

RUN ln -sf /bin/bash /bin/sh

COPY MotionDetect/ App/
WORKDIR /App
ENTRYPOINT ["tail", "-f", "/dev/null"]