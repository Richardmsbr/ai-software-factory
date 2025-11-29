.PHONY: help setup start stop restart logs clean install test

help:
	@echo "AI Software Factory - Available Commands:"
	@echo ""
	@echo "  make setup     - Initial setup (copy config, create directories)"
	@echo "  make install   - Install dependencies"
	@echo "  make start     - Start all services"
	@echo "  make stop      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - View logs"
	@echo "  make clean     - Clean up (remove containers and volumes)"
	@echo "  make test      - Run tests"
	@echo ""

setup:
	@echo "Setting up AI Software Factory..."
	@mkdir -p config logs projects
	@if [ ! -f config/.env ]; then cp config/example.env config/.env; echo "Created config/.env - Please edit with your API keys"; fi
	@echo "Setup complete!"

install:
	@echo "Installing dependencies..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	@echo "Dependencies installed!"

start:
	@echo "Starting AI Software Factory..."
	docker-compose up -d
	@echo ""
	@echo "Factory is starting..."
	@echo "Dashboard: http://localhost:3000"
	@echo "API Docs:  http://localhost:8000/api/docs"
	@echo ""
	@echo "Run 'make logs' to view logs"

stop:
	@echo "Stopping AI Software Factory..."
	docker-compose down
	@echo "Factory stopped"

restart:
	@echo "Restarting AI Software Factory..."
	docker-compose restart
	@echo "Factory restarted"

logs:
	docker-compose logs -f

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	@echo "Cleanup complete"

test:
	@echo "Running tests..."
	cd backend && pytest
	@echo "Tests complete"

status:
	@echo "Service Status:"
	@docker-compose ps
