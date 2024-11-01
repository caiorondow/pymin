# Nome do ambiente virtual
VENV = venv

# Nome do pacote de requisitos
REQUIREMENTS = requirements.txt

# Definir os comandos a serem usados
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest

# Define o comando init que cria o ambiente virtual e instala as dependências
init:
	@echo "Create virtual environment..."
	python3 -m venv $(VENV)
	@echo "Installing requirements..."
	$(PIP) install -r $(REQUIREMENTS)
	@echo "Virtual environment created and dependencies installed."

# Define o comando test que roda os testes com pytest na pasta 'test'
test:
	@echo "Run tests..."
	$(PYTEST) tests -s

# Limpeza dos arquivos compilados e ambiente virtual
clean:
	@echo "Cleanning .pyc files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Cleanning temp folders..."
	rm -rf misc/
	@echo "Cleanning virtual environment..."
	rm -rf $(VENV)
	@echo "Limpeza completa."

all: init test clean

.PHONY: init test clean