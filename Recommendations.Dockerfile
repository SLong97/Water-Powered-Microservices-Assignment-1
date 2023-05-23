FROM python:3-stretch

RUN mkdir /service

COPY protobufs/ /service/protobufs/

COPY recommendations/ /service/recommendations/

WORKDIR /service/recommendations

RUN pip install --upgrade pip

RUN pip install --trusted-host pypi.python.org -r requirements2.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/recommendations.proto

EXPOSE 50051

ENTRYPOINT [ "python", "recommendations.py" ]
