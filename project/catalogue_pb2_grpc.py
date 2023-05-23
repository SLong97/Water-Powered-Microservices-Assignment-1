# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import catalogue_pb2 as catalogue__pb2


class CataloguesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Catalogued = channel.unary_unary(
                '/Catalogues/Catalogued',
                request_serializer=catalogue__pb2.CatalogueRequest.SerializeToString,
                response_deserializer=catalogue__pb2.CatalogueResponse.FromString,
                )


class CataloguesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Catalogued(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CataloguesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Catalogued': grpc.unary_unary_rpc_method_handler(
                    servicer.Catalogued,
                    request_deserializer=catalogue__pb2.CatalogueRequest.FromString,
                    response_serializer=catalogue__pb2.CatalogueResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Catalogues', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Catalogues(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Catalogued(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Catalogues/Catalogued',
            catalogue__pb2.CatalogueRequest.SerializeToString,
            catalogue__pb2.CatalogueResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)