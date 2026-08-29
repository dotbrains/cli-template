BINARY := __PROJECT_NAME__
VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo dev)

.PHONY: build test lint install clean cover vet

build:
	VERSION=$(VERSION) mbx build --release

install:
	VERSION=$(VERSION) cargo install --path .

test:
	mbx test
	mbx test --doc

vet:
	mbx check

lint:
	mbx clippy -- -D warnings

clean:
	cargo clean

cover:
	cargo tarpaulin --out html --output-dir coverage

.DEFAULT_GOAL := build
