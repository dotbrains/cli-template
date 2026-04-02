BINARY := __PROJECT_NAME__
VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo dev)

.PHONY: build test lint install clean cover vet

build:
	VERSION=$(VERSION) cargo build --release

install:
	VERSION=$(VERSION) cargo install --path .

test:
	cargo test
	cargo test --doc

vet:
	cargo check

lint:
	cargo clippy -- -D warnings

clean:
	cargo clean

cover:
	cargo tarpaulin --out html --output-dir coverage

.DEFAULT_GOAL := build
