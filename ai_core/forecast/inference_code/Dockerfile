FROM python:3.8

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && \
    pip install flask gevent gunicorn && \
        rm -rf /root/.cache

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set up the program in the image
COPY NER /opt/program
WORKDIR /opt/program

# Make serve script executable
RUN chmod +x /opt/program/serve

# Set environment variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up nginx
RUN mkdir -p /var/log/nginx && touch /var/log/nginx/error.log
RUN ln -s /opt/program/nginx.conf /etc/nginx/conf.d/nginx.conf

EXPOSE 8080

# Define entrypoint
ENTRYPOINT ["/opt/program/serve"]