import json
import os
import openai
from semantic_router import Route
from semantic_router.encoders import OpenAIEncoder
from semantic_router.layer import RouteLayer
from dotenv import load_dotenv

# Učitaj environment varijable
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set API key directly in the OpenAI module (for semantic_router)
openai.api_key = api_key  # This is important for compatibility

# Also set environment variable
os.environ["OPENAI_API_KEY"] = api_key

print(f"API Key loaded: {api_key[:5]}...{api_key[-4:]}")

class ChatbotRouter:
	def __init__(self):
		# Učitaj podatke pitanja i odgovora
		self.load_qa_data()
		
		# Skip direct testing with OpenAI client to avoid version conflicts
		# Simply initialize the encoder and router directly
		
		# Kreiraj encoder
		self.encoder = OpenAIEncoder()
		
		# Kreiraj rute za svako pitanje
		self.routes = []
		for qa in self.qa_data["qa_pairs"]:
			self.routes.append(
				Route(
					name=f"q_{len(self.routes)}",
					utterances=[qa["question"]],
					response=qa["answer"]
				)
			)
		
		# Inicijaliziraj layer za usmjeravanje
		self.router = RouteLayer(
			encoder=self.encoder,
			routes=self.routes
		)
	
	def load_qa_data(self):
		"""Učitaj podatke pitanja i odgovora iz JSON datoteke"""
		script_dir = os.path.dirname(os.path.abspath(__file__))
		qa_path = os.path.join(script_dir, "data", "qa_data.json")
		
		with open(qa_path, 'r', encoding='utf-8') as file:
			self.qa_data = json.load(file)
	
	async def get_response(self, query: str) -> str:
		"""Dobij odgovor na temelju korisničkog upita"""
		# Pronađi najrelevantniju rutu za korisničko pitanje
		route_result = await self.router.match(query)
		
		if route_result:
			# Ako je pronađena podudarajuća ruta, vrati odgovor
			for qa in self.qa_data["qa_pairs"]:
				if qa["question"] in self.routes[int(route_result.name.split('_')[1])].utterances:
					return qa["answer"]
					
		# Ako nema podudaranja, vrati zadani odgovor
		return "Žao mi je, ne mogu odgovoriti na to pitanje. Molim kontaktirajte studentsku službu za više informacija."