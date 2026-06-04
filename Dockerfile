# The image is already built, please use the following command to run the container:
# docker start chatbot-container
# To stop the container, use:
# docker stop chatbot-container
#
# if you want to rebuild the image, use the following command:
# docker build -t chatbot-container .
# To run the container with the new image, use:
# docker run -d --name chatbot-api -p 5000:5000 chatbot-container

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /EduBuddy-Chatbot

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /EduBuddy-Chatbot/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /EduBuddy-Chatbot

EXPOSE 5000

CMD ["python", "app_fastapi.py"]