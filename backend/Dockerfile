# Using lightweight alpine image
FROM python:3.10-alpine

# Installing packages
RUN apk update

# Defining working directory and adding source code
WORKDIR /usr/src/app

COPY .env bootstrap.sh requirements.txt  ./
RUN chmod +x /usr/src/app/bootstrap.sh

COPY src ./src

# Install API dependencies
# RUN pipenv install --system --deploy
RUN pip install -r requirements.txt

# Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]