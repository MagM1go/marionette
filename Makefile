.PHONY: up down restart logs ps app-up monitoring-up app-down monitoring-down

NETWORK := marionette-observability
APP_COMPOSE := docker-compose.yml
MONITORING_COMPOSE := docker-compose.monitoring.yml

BUILD ?= 0
DETACH ?= 1

ifeq ($(BUILD),1)
	UP_BUILD := --build
else
	UP_BUILD :=
endif

ifeq ($(DETACH),1)
	UP_DETACH := -d
else
	UP_DETACH :=
endif

up:
	@docker network inspect $(NETWORK) >/dev/null 2>&1 || docker network create $(NETWORK)
	docker compose -f $(APP_COMPOSE) up $(UP_DETACH) $(UP_BUILD)
	docker compose -f $(MONITORING_COMPOSE) up $(UP_DETACH)

down:
	docker compose -f $(MONITORING_COMPOSE) down
	docker compose -f $(APP_COMPOSE) down

restart: down up

logs:
	docker compose -f $(APP_COMPOSE) logs -f

ps:
	docker compose -f $(APP_COMPOSE) ps
	docker compose -f $(MONITORING_COMPOSE) ps

app-up:
	@docker network inspect $(NETWORK) >/dev/null 2>&1 || docker network create $(NETWORK)
	docker compose -f $(APP_COMPOSE) up $(UP_DETACH) $(UP_BUILD)

monitoring-up:
	@docker network inspect $(NETWORK) >/dev/null 2>&1 || docker network create $(NETWORK)
	docker compose -f $(MONITORING_COMPOSE) up $(UP_DETACH)

app-down:
	docker compose -f $(APP_COMPOSE) down

monitoring-down:
	docker compose -f $(MONITORING_COMPOSE) down
