.PHONY: setup run-backend run-frontend run clean

# Settings for virtual environment
VENV_DIR = venv
VENV_PYTHON = $(VENV_DIR)/Scripts/python
VENV_PIP = $(VENV_DIR)/Scripts/pip

# System Python for setup
PYTHON = python
PIP = pip

# Postavljanje virtualnog okruženja
setup:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PIP) install -r requirements.txt

# Pokretanje backend aplikacije
run-backend:
	$(VENV_PYTHON) -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Pokretanje frontend aplikacije
run-frontend:
	cd frontend && $(VENV_PYTHON) -m http.server 8080

# Pokretanje i backend i frontend (u paraleli)
run:
	@echo "Pokretanje backend i frontend servera..."
	@bash -c "./$(VENV_DIR)/Scripts/python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &"
	@bash -c "cd frontend && ../$(VENV_DIR)/Scripts/python -m http.server 8080 &"
	@echo "Serveri pokrenuti. Pritisnite Ctrl+C za zaustavljanje."
	@bash -c "read -p ''"

# Brisanje virtualnog okruženja
clean:
	@echo "Brisanje virtualnog okruženja..."
	rm -rf $(VENV_DIR)
	@echo "Virtualno okruženje obrisano. Pokrenite 'make setup' za kreiranje novog."