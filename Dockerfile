From python:3.7
# import bash / flask
RUN  pip install --upgrade pip && \
     pip install flask && \
     pip install Pillow && \
     pip install requests==2.22.0 && \
     pip install tensorflow==1.14.0 && \ 
     pip install tensorflow-serving-api==1.13.0

ENV FLASK_APP=/gateway/main.py \
    EXPOSE_PORT=5000 

COPY ./gateway /gateway

WORKDIR /gateway

ENTRYPOINT [ "/bin/bash","-c","flask run --host 0.0.0.0 --port $EXPOSE_PORT"]

#CMD ["--port","$EXPOSE_PORT"]

EXPOSE ${EXPOSE_PORT}
EXPOSE 1-20000
