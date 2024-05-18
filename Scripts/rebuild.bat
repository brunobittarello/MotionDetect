set PORT=80
set ENV=Development
set IMAGE_NAME=motiondetect:latest
set CONTAINER_NAME=motiondetect-local
docker build -t %IMAGE_NAME% .
call Scripts/renew.bat