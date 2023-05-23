from concurrent import futures
import random
import grpc

from catalogue_pb2 import (
    GameStatus,
    CatalogueRecommendation,
    CatalogueResponse,
)

import catalogue_pb2_grpc


games_by_category = {

    GameStatus.NEW:[
    
        CatalogueRecommendation(id=1, 
                           title="Horizon Forbidden West", 
                           developer="Guerrilla Games", 
                           description="Horizon Forbidden West is an action role-playing game developed by Guerrilla Games and published by Sony Interactive Entertainment. It is the sequel to Horizon Zero Dawn and continues the story of Aloy, a young huntress in a world overrun by dangerous robotic creatures.", 
                           rating="★★★★",
                           cover="https://blog.playstation.com/uploads/2023/03/d69b393523b7487cd87b4d938133b2370a07cf8d.jpeg",
                           price="$59.99", 
                           sale="$49.99"),
                           
        CatalogueRecommendation(id=2, 
                           title="Elden Ring", 
                           developer="FromSoftware", 
                           description="Elden Ring is an action role-playing game developed by FromSoftware and published by Bandai Namco Entertainment. It is created in collaboration with George R. R. Martin and is set in a new world created by Hidetaka Miyazaki, the creator of the Dark Souls series.", 
                           rating="★★★★★",
                           cover="https://image.api.playstation.com/vulcan/ap/rnd/202108/0410/0Jz6uJLxOK7JOMMfcfHFBi1D.png",
                           price="$59.99", 
                           sale="$49.99"),
                           
        CatalogueRecommendation(id=3, 
                           title="Stray", 
                           developer="BlueTwelve Studio", 
                           description="Stray is an action-adventure game developed by BlueTwelve Studio and published by Annapurna Interactive. The game is set in a futuristic, neon-lit city and follows the story of a stray cat who gets separated from its family and must navigate the city to find its way home.", 
                           rating="★★★★",
                           cover="https://image.api.playstation.com/vulcan/ap/rnd/202206/0300/E2vZwVaDJbhLZpJo7Q10IyYo.png",
                           price="$49.99", 
                           sale="$45.99"),

    ],

    GameStatus.TRENDING: [

        CatalogueRecommendation(id=4, 
                           title="Hitman 3", 
                           developer="IO Interactive", 
                           description="Hitman 3 is a stealth game where the player takes on the role of the legendary assassin Agent 47, as he embarks on a globe-trotting adventure to eliminate high-profile targets.", 
                           rating="★★★★", 
                           cover="https://d1w82usnq70pt2.cloudfront.net/wp-content/uploads/2021/01/hitman3banner.jpg", 
                           price="$59.99", 
                           sale="$29.99"),

        CatalogueRecommendation(id=5, 
                           title="Forza Horizon 5", 
                           developer="Playground Games", 
                           description="Forza Horizon 5 is an open-world racing game where players can explore the vast world, compete in various races and events, and customize their cars to their liking.", 
                           rating="★★★★",
                           cover="https://cdn.cloudflare.steamstatic.com/steam/apps/1551360/capsule_616x353.jpg?t=1677534139",
                           price="$59.99", 
                           sale="$45.99"),

        CatalogueRecommendation(id=6, 
                           title="LEGO Star Wars: The Skywalker Saga", 
                           developer="Traveller's Tales", 
                           description="LEGO Star Wars: The Skywalker Saga is an action-adventure game that covers all nine films of the Star Wars saga. Players can take control of numerous characters from the films and experience their adventures in a lighthearted LEGO-style.", 
                           rating="★★★★",
                           cover="https://www.greenmangaming.com/blog/wp-content/uploads/2022/03/lego-star-wars-the-skywalker-saga-release-date-system-requirements-gameplay-trailers-890x606.jpg",
                           price="$45.99", 
                           sale="$20.99"),

    ],

    GameStatus.SALE: [

        CatalogueRecommendation(id=7, 
                           title="Marvel's Midnight Suns", 
                           developer="Firaxis Games", 
                           description="Marvel's Midnight Suns is a tactical RPG that features iconic Marvel characters like Wolverine, Iron Man, and Captain America as they team up to save the world from the demonic Lilith.", 
                           rating="★★★",
                           cover="https://cdn.cloudflare.steamstatic.com/steam/apps/368260/capsule_616x353.jpg?t=1679414785", 
                           price="$59.99", 
                           sale="$30.00"),

        CatalogueRecommendation(id=8, 
                           title="Gotham Knights", 
                           developer="WB Games Montreal", 
                           description="Gotham Knights is an action RPG set in the Batman universe. The game features playable characters like Nightwing, Batgirl, Robin, and Red Hood as they protect Gotham City in the aftermath of Batman's death.", 
                           rating="★★★",
                           cover="https://cdn1.epicgames.com/offer/05057ec2d5ea43c3b0701cc1518e0577/EGS_GothamKnights_WarnerBrosGamesMontreal_S2_1200x1600-5a46b442e57afa637f013bbc09fe5487", 
                           price="$49.99", 
                           sale="$20.00"),

        CatalogueRecommendation(id=9, 
                           title="Evil Dead: The Game", 
                           developer="Boss Team Games", 
                           description="Evil Dead: The Game is a multiplayer action game that lets players team up to take on hordes of evil Deadites. The game features iconic characters from the Evil Dead franchise like Ash Williams.", 
                           rating="★★★",
                           cover="https://image.api.playstation.com/vulcan/ap/rnd/202109/2814/DU8n42KdlEEvLtIJFHNEAvQX.jpg", 
                           price="$35.99", 
                           sale="$18.00"),

    ],

}


class CatalogueService(catalogue_pb2_grpc.CataloguesServicer):

    def Catalogued(self, request, context):

        if request.category not in games_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")


        games_for_category = games_by_category[request.category]
        num_results = min(request.max_results, len(games_for_category))
        games_catalogue = random.sample(games_for_category, num_results)


        return CatalogueResponse(recommendations=games_catalogue)
    

def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalogue_pb2_grpc.add_CataloguesServicer_to_server(CatalogueService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

