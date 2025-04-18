import json
import os
from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.layer import RouteLayer

class ChatbotRouter:
    def __init__(self):
        # Učitaj podatke pitanja i odgovora
        self.load_qa_data()
        
        # Kreiraj HuggingFace encoder umjesto OpenAI encodera
        # Koristimo all-MiniLM-L6-v2 model koji je mali, brz i daje dobre rezultate
        print("Inicijalizacija HuggingFace encodera...")
        self.encoder = HuggingFaceEncoder(model_name="all-MiniLM-L6-v2")
        print("HuggingFace encoder inicijaliziran.")
        
        # Kreiraj rute za svako pitanje
        print("Kreiranje ruta...")
        self.routes = []
        for qa in self.qa_data["qa_pairs"]:
            self.routes.append(
                Route(
                    name=f"q_{len(self.routes)}",
                    utterances=[qa["question"]],
                    response=qa["answer"]
                )
            )
        print(f"Kreirano {len(self.routes)} ruta.")
        
        # Inicijaliziraj layer za usmjeravanje
        print("Inicijalizacija RouteLayer-a...")
        self.router = RouteLayer(
            encoder=self.encoder,
            routes=self.routes
        )
        print("RouteLayer inicijaliziran.")
    
    def load_qa_data(self):
        """Učitaj podatke pitanja i odgovora iz JSON datoteke"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        qa_path = os.path.join(script_dir, "data", "qa_data.json")
        
        print(f"Učitavanje podataka iz: {qa_path}")
        with open(qa_path, 'r', encoding='utf-8') as file:
            self.qa_data = json.load(file)
        print(f"Učitano {len(self.qa_data['qa_pairs'])} pitanja i odgovora.")
    
    async def get_response(self, query: str) -> str:
        """Dobij odgovor na temelju korisničkog upita"""
        print(f"Obrada upita: '{query}'")
        # Pronađi najrelevantniju rutu za korisničko pitanje
        route_result = self.router(query)
        
        if route_result:
            print(f"Pronađena ruta: {route_result.name}")
            print(f"Route result attributes: {dir(route_result)}")
            # Ako je pronađena podudarajuća ruta, vrati odgovor
            try:
                route_index = int(route_result.name.split('_')[1])
                for qa in self.qa_data["qa_pairs"]:
                    if qa["question"] in self.routes[route_index].utterances:
                        return qa["answer"]
            except (ValueError, IndexError, AttributeError) as e:
                print(f"Error accessing route: {e}")
        else:
            print("Nije pronađena odgovarajuća ruta.")           
        # Ako nema podudaranja, vrati zadani odgovor
        return "Žao mi je, ne mogu odgovoriti na to pitanje. Molim kontaktirajte studentsku službu za više informacija."