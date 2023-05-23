import fileinput

with fileinput.FileInput('project/recommendations_pb2_grpc.py', inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace('import recommendations_pb2 ', 'from . import recommendations_pb2 '), end='')