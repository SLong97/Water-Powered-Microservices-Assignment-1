FROM python:3-stretch

RUN mkdir /service

COPY protobufs/ /service/protobufs/

COPY catalogue/ /service/catalogue/

WORKDIR /service/catalogue

RUN pip install --upgrade pip

RUN pip install --trusted-host pypi.python.org -r requirements3.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/catalogue.proto

EXPOSE 50052

ENTRYPOINT [ "python", "catalogue.py" ]