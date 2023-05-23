from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
import os
import grpc
import pika
import datetime

from . import recommendations_pb2 as recommendations_pb2
from project.recommendations_pb2 import GameCategory, RecommendationRequest
from project.recommendations_pb2_grpc import RecommendationsStub

recommendationshost = os.getenv("RECOMMENDATIONS_HOST")
recommendations_channel = grpc.insecure_channel(f'{recommendationshost}:50051')
recommendations_client = RecommendationsStub(recommendations_channel)


from . import catalogue_pb2 as catalogue_pb2
from project.catalogue_pb2 import GameStatus, CatalogueRequest
from project.catalogue_pb2_grpc import CataloguesStub

cataloguehost = os.getenv("CATALOGUE_HOST")
catalogue_channel = grpc.insecure_channel(f'{cataloguehost}:50052')
catalogue_client = CataloguesStub(catalogue_channel)

credentials = pika.PlainCredentials('admin', 'admin')

# establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials, heartbeat=0))
channel = connection.channel()

# declare the queue to publish messages to
channel.queue_declare(queue='user_activity')


main = Blueprint('main', __name__)


@main.before_request
def log_user_activity():
    page = request.path
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data = "Visited: " + page + " - " + "Date Time: " + formatted_datetime

    channel.basic_publish(exchange='',
                          routing_key='user_activity',
                          body=data)



@main.route('/')
def index():

    # page = request.path
    # current_datetime = datetime.datetime.now()
    # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # data = page + " : " + formatted_datetime

    # channel.basic_publish(exchange='',
    #                     routing_key='user_activity',
    #                     body=data)

    

    return render_template('index.html')

@main.route('/store')
def store():

    # page = request.path
    # current_datetime = datetime.datetime.now()
    # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # data = page + " : " + formatted_datetime

    # channel.basic_publish(exchange='',
    #                     routing_key='user_activity',
    #                     body=data)

    catalogue_request1 = CatalogueRequest(user_id=1, category=GameStatus.NEW, max_results=3)
    catalogue_response1 = catalogue_client.Catalogued(catalogue_request1)

    catalogue_request2 = CatalogueRequest(user_id=1, category=GameStatus.TRENDING, max_results=3)
    catalogue_response2 = catalogue_client.Catalogued(catalogue_request2)

    catalogue_request3 = CatalogueRequest(user_id=1, category=GameStatus.SALE, max_results=3)
    catalogue_response3 = catalogue_client.Catalogued(catalogue_request3)


    return render_template('store.html',
                           NEW=catalogue_response1.recommendations,
                           TRENDING=catalogue_response2.recommendations,
                           SALE=catalogue_response3.recommendations)

@main.route('/profile')
@login_required
def profile():
    # consume the messages from the queue
    messages = []
    method_frame, header_frame, body = channel.basic_get(queue='user_activity')
    while method_frame:
        messages.append(body.decode("utf-8"))
        channel.basic_ack(method_frame.delivery_tag)
        method_frame, header_frame, body = channel.basic_get(queue='user_activity')

    return render_template('profile.html', name=current_user.username, rabbit_messages=messages)


@main.route('/recommendations')
@login_required
def recommendations():

    # page = request.path
    # current_datetime = datetime.datetime.now()
    # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # data = page + " : " + formatted_datetime

    # channel.basic_publish(exchange='',
    #                     routing_key='user_activity',
    #                     body=data)

    recommendations_request1 = RecommendationRequest(user_id=1, category=GameCategory.HORROR, max_results=3)
    recommendations_response1 = recommendations_client.Recommend(recommendations_request1)

    recommendations_request2 = RecommendationRequest(user_id=1, category=GameCategory.ADVENTURE, max_results=3)
    recommendations_response2 = recommendations_client.Recommend(recommendations_request2)

    recommendations_request3 = RecommendationRequest(user_id=1, category=GameCategory.SIMULATION, max_results=3)
    recommendations_response3 = recommendations_client.Recommend(recommendations_request3)


    return render_template('recommendations.html', 
                           HORROR=recommendations_response1.recommendations,
                           ADVENTURE=recommendations_response2.recommendations,
                           SIMULATION=recommendations_response3.recommendations)
