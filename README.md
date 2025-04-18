# sembot

Chatbot koji koristi Semantic Router i FastAPI za odgovaranje na upite korisnika aplikacije o fakultetu.

## Opis

Ovaj projekt implementira jednostavni chatbot za odgovaranje na česta pitanja studenata fakulteta. Backend koristi FastAPI za API endpointe i Semantic Router za pronalaženje najboljeg odgovora na temelju semantičke sličnosti. Frontend je implementiran koristeći HTML, CSS i JavaScript.

## Značajke

- Semantičko pretraživanje pitanja i odgovora
- Jednostavno sučelje za chat
- Lako proširivi sustav dodavanjem novih pitanja i odgovora

## Struktura projekta

```
chatbot-fakultet/
├── Makefile               # Komande za upravljanje projektom
├── requirements.txt       # Python ovisnosti
├── .env                   # Konfiguracijske varijable okruženja
├── backend/
│   ├── main.py           # FastAPI glavna aplikacija
│   ├── router.py         # Semantic Router implementacija
│   └── data/
│       └── qa_data.json  # Podaci pitanja i odgovora
└── frontend/
    ├── index.html
    ├── static/
        ├── css/
        │   └── style.css
        └── js/
            └── script.js
```

## Preduvjeti

- Python 3.8+
- OpenAI API ključ (za Semantic Router)

## Postavljanje

1. Klonirajte repozitorij:

   ```
   git clone https://github.com/username/fakultetski-chatbot.git
   cd fakultetski-chatbot
   ```

2. Uredite `.env` datoteku i dodajte svoj OpenAI API ključ:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Pokrenite postavke koristeći Makefile:
   ```
   make setup
   ```

## Pokretanje

Za pokretanje i backend i frontend servera:

```
make run
```

Za pokretanje samo backend servera:

```
make run-backend
```

Za pokretanje samo frontend servera:

```
make run-frontend
```

Nakon pokretanja, aplikaciji možete pristupiti putem:

- Backend: http://localhost:8000
- Frontend: http://localhost:8080

## Prilagodba pitanja i odgovora

Pitanja i odgovore možete urediti u datoteci `backend/data/qa_data.json`. Nakon uređivanja, potrebno je ponovno pokrenuti backend kako bi promjene bile učitane.

## Licenca

Ovaj projekt je pod [MIT licencom](LICENSE).
