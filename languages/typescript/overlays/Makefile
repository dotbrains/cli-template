.PHONY: build test lint install clean dev typecheck format

.DEFAULT_GOAL := build

node_modules/package.json:
	npm install

dev: node_modules/package.json

build: dev
	npm run build

test: dev
	npm run test

typecheck: dev
	npm run typecheck

lint: dev
	npm run lint

format: dev
	npm run format

install: dev
	npm link

clean:
	rm -rf node_modules dist coverage
