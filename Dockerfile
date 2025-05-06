FROM public.ecr.aws/docker/library/python:3.12-alpine

RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app
COPY . /app/
    
RUN pip install -r src/requirements.txt

EXPOSE 5000

CMD ["python3", "src/application.py"]