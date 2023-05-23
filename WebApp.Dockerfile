# Use an official Python runtime as a parent image
FROM python:3-stretch

# Set the working directory to /app
RUN mkdir /service

# Copy the current directory contents into the container at /app
COPY . /service/

WORKDIR /service/project

RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/recommendations.proto

WORKDIR /service/

# Expose the port for the Flask app
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP project

# Run the command to start the Flask app
#CMD ["flask", "run", "--host", "0.0.0.0"]

COPY wait-for-it.sh ./
COPY start_script.sh ./
COPY run.sh ./
RUN chmod a+x start_script.sh

CMD ["./start_script.sh"]
