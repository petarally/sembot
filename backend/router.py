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
        
        # Kategoriziraj pitanja za bolje predviđanje sljedećih pitanja
        self.categorize_questions()
    
    def load_qa_data(self):
        """Učitaj podatke pitanja i odgovora iz JSON datoteke"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        qa_path = os.path.join(script_dir, "data", "qa_data.json")
        
        print(f"Učitavanje podataka iz: {qa_path}")
        with open(qa_path, 'r', encoding='utf-8') as file:
            self.qa_data = json.load(file)
        print(f"Učitano {len(self.qa_data['qa_pairs'])} pitanja i odgovora.")
    
    def categorize_questions(self):
        """Kategorizira pitanja po temama za predviđanje sljedećih pitanja"""
        self.categories = {
            "upisi": [],
            "ispiti": [], 
            "nastava": [],
            "kontakt": [],
            "skolarina": [],
            "studijski_programi": [],
            "sveuciliste_info": [],
            "studiranje": []
        }
        
        # Ključne riječi za kategorizaciju
        category_keywords = {
            "upisi": ["upis", "prijav", "dokument", "uvjet"],
            "ispiti": ["ispit", "rokovi", "kolokvij", "prijav", "završni", "diplomski rad"],
            "nastava": ["raspored", "predavanje", "nastav", "akademsk", "kalendar", "online"],
            "kontakt": ["kontakt", "e-mail", "email", "telefon", "studentsk", "služb"],
            "skolarina": ["školarin", "plaćanj", "rata", "popust", "stipendij"],
            "studijski_programi": ["program", "fakultet", "studij", "ekonomij", "informatik", "medicin"],
            "sveuciliste_info": ["sveučilišt", "jurja", "dobril", "pul", "adres", "web"],
            "studiranje": ["ECTS", "bod", "godina", "potvrda", "studiranj", "e-učenje"]
        }
        
        # Kategoriziraj pitanja
        for qa in self.qa_data["qa_pairs"]:
            question = qa["question"].lower()
            
            # Provjeri za svaku kategoriju
            for category, keywords in category_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in question:
                        self.categories[category].append(qa["question"])
                        break
    
    def is_university_related(self, query: str) -> bool:
        """
        Provjerava je li korisničko pitanje vezano za sveučilište.
        
        Args:
            query (str): Korisničko pitanje
            
        Returns:
            bool: True ako je pitanje vezano uz sveučilište, False inače
        """
        # Ključne riječi specifične za akademski kontekst i Sveučilište Jurja Dobrile u Puli
        university_keywords = [
            # Opći akademski termini
            "fakultet", "sveučilište", "studij", "profesor", "predavanje", "ispit", "kolokvij",
            "rokovi", "nastava", "upisi", "predmet", "semestar", "akademski", "diploma",
            "mentor", "studentski", "knjižnica", "dom", "X-ica", "iksica", "stipendija", "ECTS",
            "bologna", "dekan", "referada", "učionica", "demonstrator", "asistent",
            
            # Specifični za Sveučilište u Puli
            "pula", "jurja dobrile", "unipu", "studomat", "školarina", "potvrda", "informatika",
            "ekonomija", "medicina", "turizam", "glazba", "muzička", "online", "upis", "kalendar",
            
            # Dodatni akademski pojmovi
            "diplomski", "preddiplomski", "završni", "rad", "teza", "disertacija", "obrana",
            "erasmus", "razmjena", "ured za studente", "zagrebačka", "student", "ispitni rok",
            "demonstratura", "skript", "literatura", "udžbenik", "indeks", "ISVU", "AAI",
            "seminar", "seminarski", "esej", "projekt", "ocjena", "bodovi", "kolega", "godina",
            "tema", "istraživanje", "bibliografija", "citiranje", "reference", "metodologija",
            "apsolvent", "brucoš", "alumni", "prijavnica", "upitnik", "studiranje", "apsolvirati",
            "ispitni", "stranica", "prijava", "status", "uvjeti", "upisati", "pisati", "napisati",
            "autor", "nastavnik", "konzultacije", "program", "obveze", "obveza", "literatura",
            "zbornica", "menza", "blagavaona", "prijemni", "bodovanje"
        ]
        
        # Pretvori u mala slova radi lakše usporedbe
        query_lower = query.lower()
        
        # Provjeri sadrži li pitanje bilo koju ključnu riječ vezanu za sveučilište
        for keyword in university_keywords:
            if keyword.lower() in query_lower:
                return True
        
        # Dodatna provjera za česte fraze vezane uz studiranje koje ne sadrže nužno ključne riječi
        common_phrases = [
            "kako napisati", "kako predati", "kako dobiti", "kako se prijaviti", 
            "gdje predati", "gdje pronaći", "koji su uvjeti", "koji su rokovi",
            "kada je rok", "kada počinje", "kada završava", "što trebam",
            "što moram", "trebam li", "moram li", "mogu li", "gdje je",
            "koja je procedura", "kako funkcionira", "kako radi"
        ]
        
        # Ako ima neku od čestih fraza, vjerojatno je vezano za sveučilište u kontekstu chatbota
        for phrase in common_phrases:
            if phrase in query_lower:
                return True
        
        return False

    def get_default_response(self) -> dict:
        """
        Vraća standardni odgovor kada korisnik postavi pitanje izvan teme sveučilišta.
        
        Returns:
            dict: Standardni odgovor s prijedlogom za povratak na temu sveučilišta
        """
        default_response = {
            "text": (
                "Izgleda da je vaše pitanje izvan okvira informacija o Sveučilištu Jurja Dobrile u Puli. "
                "Ja sam specijaliziran za pružanje informacija o studijskim programima, rokovima, "
                "događanjima na fakultetu, postupcima upisa i drugim temama vezanim uz Sveučilište. "
                "Možete me pitati o rasporedu nastave, kontakt informacijama, rokovima za predaju radova "
                "ili bilo čemu drugom vezanom uz studiranje na Sveučilištu u Puli."
            ),
            "suggested_questions": [
                "Kako mogu kontaktirati studentsku službu?",
                "Gdje mogu pronaći raspored predavanja?",
                "Koji su rokovi za prijavu ispita?"
            ]
        }
        return default_response
    
    def generate_next_questions(self, query: str, answer: str) -> list:
        """
        Generira prijedloge za sljedeća pitanja na temelju trenutnog pitanja i odgovora.
        
        Args:
            query (str): Trenutno korisničko pitanje
            answer (str): Odgovor na trenutno pitanje
            
        Returns:
            list: Lista prijedloga za sljedeća pitanja
        """
        # Pretvori u mala slova radi lakše usporedbe
        query_lower = query.lower()
        
        # Definiraj tipove pitanja koji bi mogli slijediti trenutno
        related_categories = []
        
        # Provjeri kojem tipu pripada trenutno pitanje
        if any(word in query_lower for word in ["upis", "prijav", "uvjet"]):
            related_categories = ["upisi", "skolarina", "studijski_programi"]
        elif any(word in query_lower for word in ["ispit", "kolokvij", "završni", "diplomski rad"]):
            related_categories = ["ispiti", "nastava", "studiranje"]
        elif any(word in query_lower for word in ["raspored", "predavanje", "nastav", "akademsk"]):
            related_categories = ["nastava", "studiranje", "kontakt"]
        elif any(word in query_lower for word in ["kontakt", "e-mail", "telefon", "služb"]):
            related_categories = ["kontakt", "sveuciliste_info"]
        elif any(word in query_lower for word in ["školarin", "plaćanj", "stipendij"]):
            related_categories = ["skolarina", "upisi", "kontakt"]
        elif any(word in query_lower for word in ["program", "fakultet", "studij"]):
            related_categories = ["studijski_programi", "upisi", "sveuciliste_info"]
        elif any(word in query_lower for word in ["sveučilišt", "jurja", "dobril", "pul"]):
            related_categories = ["sveuciliste_info", "kontakt", "studijski_programi"]
        elif any(word in query_lower for word in ["ECTS", "bod", "godina", "potvrda"]):
            related_categories = ["studiranje", "ispiti", "kontakt"]
        else:
            # Ako ne možemo odrediti kategoriju, koristimo općenite
            related_categories = ["sveuciliste_info", "kontakt", "studijski_programi"]
        
        suggested_questions = []
        
        # Iz svake relevantne kategorije uzmi po jedno pitanje ako postoji
        for category in related_categories:
            if self.categories[category] and len(self.categories[category]) > 0:
                # Ako kategorija ima pitanja, odaberi prvo koje nije trenutno pitanje
                for question in self.categories[category]:
                    if question != query and question not in suggested_questions:
                        suggested_questions.append(question)
                        break
        
        # Ako nismo uspjeli dobiti dovoljno pitanja, dodaj neka općenita
        if len(suggested_questions) < 3:
            general_questions = [
                "Koje je službeno ime Sveučilišta u Puli?",
                "Kako mogu kontaktirati studentsku službu?",
                "Gdje mogu pronaći raspored predavanja?",
                "Koji su rokovi za prijavu ispita?",
                "Koje fakultete ima Sveučilište Jurja Dobrile u Puli?"
            ]
            
            for question in general_questions:
                if question != query and question not in suggested_questions:
                    suggested_questions.append(question)
                    if len(suggested_questions) >= 3:
                        break
        
        # Vrati maksimalno 3 prijedloga
        return suggested_questions[:3]

    async def get_response(self, query: str) -> dict:
        """
        Dobij odgovor na temelju korisničkog upita
        
        Args:
            query (str): Korisničko pitanje
            
        Returns:
            dict: Rječnik koji sadrži tekst odgovora i prijedloge za sljedeća pitanja
        """
        print(f"Obrada upita: '{query}'")
        
        # Provjeri je li pitanje vezano za sveučilište
        if not self.is_university_related(query):
            print("Pitanje nije vezano za sveučilište, vraćam standardni odgovor.")
            return self.get_default_response()
        
        # Pronađi najrelevantniju rutu za korisničko pitanje
        route_result = self.router(query)
        
        if route_result:
            print(f"Pronađena ruta: {route_result.name}")
            
            # Ako je pronađena podudarajuća ruta, vrati odgovor
            try:
                route_index = int(route_result.name.split('_')[1])
                for qa in self.qa_data["qa_pairs"]:
                    if qa["question"] in self.routes[route_index].utterances:
                        answer = qa["answer"]
                        # Generiraj prijedloge za sljedeća pitanja
                        suggested_questions = self.generate_next_questions(query, answer)
                        
                        return {
                            "text": answer,
                            "suggested_questions": suggested_questions
                        }
            except (ValueError, IndexError, AttributeError) as e:
                print(f"Error accessing route: {e}")
        
        # Ako nema podudaranja, vrati zadani odgovor s prijedlozima
        print("Nije pronađena odgovarajuća ruta.")
        return {
            "text": "Žao mi je, ne mogu precizno odgovoriti na to pitanje. Za dodatne informacije, možete kontaktirati studentsku službu na ured-za-studente@unipu.hr ili telefonom na 052/377-006.",
            "suggested_questions": [
                "Kako mogu kontaktirati studentsku službu?",
                "Gdje mogu pronaći akademski kalendar?",
                "Koja je web stranica Sveučilišta Jurja Dobrile?"
            ]
        }