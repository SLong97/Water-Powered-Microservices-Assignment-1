import fileinput

with fileinput.FileInput('project/catalogue_pb2_grpc.py', inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace('import catalogue_pb2', 'from . import catalogue_pb2'), end='')