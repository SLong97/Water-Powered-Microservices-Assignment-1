from concurrent import futures
import random
import grpc

from recommendations_pb2 import (
    GameCategory,
    GameRecommendation,
    RecommendationResponse,
)

import recommendations_pb2_grpc


games_by_category = {

    GameCategory.HORROR:[

        GameRecommendation(id=1, title="Outlast 2", developer="Red Barrels", 
                           description="A first-person psychological horror game set in the Arizona desert where players assume the role of a journalist investigating a cult.", 
                           rating="★★★★"),

        GameRecommendation(id=2, title="Resident Evil 7: Biohazard", developer="Capcom", 
                           description="A survival horror game that takes place in Louisiana, where the player takes on the role of Ethan Winters, as he searches for his wife Mia.", 
                           rating="★★★★"),

        GameRecommendation(id=3, title="Alien: Isolation", developer="Creative Assembly", 
                           description="A survival horror game set in the Alien universe, where players control Amanda Ripley as she tries to survive and evade a Xenomorph.", 
                           rating="★★★★"),

    ],

    GameCategory.ADVENTURE: [

        GameRecommendation(id=4, title="The Witcher 3: Wild Hunt", developer="CD Projekt Red", 
                           description="An open-world RPG set in a dark fantasy world, where players control Geralt of Rivia as he hunts monsters and solves conflicts.", 
                           rating="★★★★★"),

        GameRecommendation(id=5, title="Life is Strange", developer="Dontnod Entertainment", 
                           description="A narrative-driven adventure game where the player controls Max Caulfield, a high school senior who discovers she has the ability to rewind time.", 
                           rating="★★★★"),

        GameRecommendation(id=6, title="Firewatch", developer="Campo Santo", 
                           description="A first-person adventure game where players control Henry, a fire lookout in Wyoming, as he investigates strange occurrences in the wilderness.", 
                           rating="★★★"),

    ],

    GameCategory.SIMULATION: [

        GameRecommendation(id=7, title="Cities: Skylines", developer="Colossal Order", 
                           description="A city-building simulation game where players can design and manage their own city, including road networks, public services, and taxes.", 
                           rating="★★★★"),

        GameRecommendation(id=8, title="Euro Truck Simulator 2", developer="SCS Software", 
                           description="A truck driving simulation game that allows players to drive various trucks across Europe, making deliveries and managing their own trucking company.", 
                           rating="★★★★"),

        GameRecommendation(id=9, title="Kerbal Space Program", developer="Squad", 
                           description="A space flight simulation game where players design and launch their own spacecraft, exploring the solar system and completing missions.", 
                           rating="★★★★★"),

    ],

}


class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):

    def Recommend(self, request, context):

        if request.category not in games_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")


        games_for_category = games_by_category[request.category]
        num_results = min(request.max_results, len(games_for_category))
        games_to_recommend = random.sample(games_for_category, num_results)


        return RecommendationResponse(recommendations=games_to_recommend)
    

def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

