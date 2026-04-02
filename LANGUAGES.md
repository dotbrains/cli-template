# Language Selection Guide

This guide helps AI agents choose the best language for a new CLI project. Read the project requirements and evaluate each factor below.

## Quick Decision Matrix

| Factor | Go | Python | Rust | TypeScript |
|---|---|---|---|---|
| Cold start time | Fast | Slow (interpreter) | Instant | Fast (V8) |
| Binary size | Small (~10MB) | N/A (needs Python) | Tiny (~2MB) | N/A (needs Node) |
| Distribution | Single binary | Needs `pip`/Python | Single binary | Needs `npm`/Node |
| Rapid prototyping | Good | **Best** | Slowest | Good |
| Performance | Great | Adequate | **Best** | Good |
| Error handling | Explicit (`error`) | Exceptions | `Result<T, E>` | Exceptions |
| Concurrency | Goroutines (easy) | asyncio (awkward) | async/await | async/await (easy) |
| Ecosystem for CLIs | Cobra (excellent) | Click (excellent) | Clap (excellent) | Commander (great) |
| Learning curve | Low | Low | Medium-High | Low |
| Type safety | Strong (generics) | Optional (mypy) | Strict (borrow) | Strict (structural) |
| Memory safety | GC | GC | Ownership | GC |

## When to Choose Go

**Choose Go when:**
- You need a single binary that "just works" on any machine
- The team is comfortable with Go
- You want fast iteration with good performance
- The CLI does network I/O (HTTP APIs, webhooks)
- You want excellent cross-compilation out of the box
- The CLI needs concurrency (parallel API calls, watchers)

**Go is ideal for:**
- DevOps / infrastructure tools
- API wrappers and clients
- File processing with I/O bound workloads
- Tools that need to be installed via `go install`
- CLIs that integrate with Kubernetes/cloud ecosystems

**Avoid Go when:**
- You need complex data science / ML libraries
- Rapid prototyping with REPL-style iteration is critical
- The team only knows Python

## When to Choose Python

**Choose Python when:**
- Rapid prototyping and iteration speed is the priority
- The CLI wraps data science, ML, or scientific libraries
- The team is primarily Python developers
- The CLI is a glue tool that orchestrates other processes
- Rich text processing or scripting is involved
- The CLI will be used in Jupyter/Python environments

**Python is ideal for:**
- Data processing pipelines
- Wrappers around Python libraries (pandas, requests, boto3)
- Internal tools where startup time doesn't matter
- CLIs that ship alongside a Python library
- Automation scripts that need rich text/regex handling

**Avoid Python when:**
- Cold start time matters (>200ms overhead)
- Users can't be expected to have Python installed
- You need a single distributable binary
- Performance-critical computation is the core task

## When to Choose Rust

**Choose Rust when:**
- Performance and resource efficiency are critical
- The CLI must have a tiny binary footprint
- Memory safety without GC is important
- You're building a "once and done" tool people install once
- The CLI processes large files or data streams
- Startup time must be near-instant

**Rust is ideal for:**
- File format converters and processors
- System utilities (find, grep, cat replacements)
- Security-sensitive tools
- CLIs that run in CI/CD pipelines (speed matters)
- Tools that need to be embedded or called frequently
- Anything where "fast and correct" matters more than "fast to write"

**Avoid Rust when:**
- Development speed is more important than runtime speed
- The team isn't comfortable with Rust's ownership model
- You need rapid prototyping and frequent pivots
- The project is a quick prototype or throwaway tool

## When to Choose TypeScript

**Choose TypeScript when:**
- The team is primarily JavaScript/TypeScript developers
- The CLI interacts with web APIs, npm packages, or Node.js ecosystem
- You want strong typing without learning a new language
- The CLI ships alongside a JavaScript/TypeScript library
- You need the largest package ecosystem (npm)
- The CLI is a DevOps tool used in Node.js-heavy environments

**TypeScript is ideal for:**
- API wrappers and webhook handlers
- Build tools and dev servers
- CLIs that ship alongside npm packages
- Tools for the JavaScript/Node.js ecosystem
- Rapid prototyping with strong typing
- Teams transitioning from JavaScript

**Avoid TypeScript when:**
- You need a single distributable binary (without extra tooling)
- Cold start time is critical (Node.js has ~50ms overhead)
- Users can't be expected to have Node.js installed
- Performance-critical computation is the core task
- Memory efficiency is important

## Decision Flowchart

```
Is this a quick prototype or throwaway?
  YES → Python
  NO ↓

Do users need to install without dependencies?
  YES → Go or Rust
  NO ↓

Is startup time critical (<50ms)?
  YES → Rust
  NO ↓

Is the team already proficient in one language?
  YES → Use that language
  NO ↓

Does it need to integrate with npm/Node.js/web ecosystem?
  YES → TypeScript
  NO ↓

Does it need to integrate with Python/ML/data ecosystem?
  YES → Python
  NO ↓

Does it need to integrate with cloud/K8s ecosystem?
  YES → Go
  NO ↓

Default → Go (best balance of productivity and performance)
```

## Technology Stack Comparison

| Component | Go | Python | Rust | TypeScript |
|---|---|---|---|---|
| CLI framework | Cobra | Click | Clap | Commander |
| Config format | YAML (gopkg.in/yaml.v3) | YAML (PyYAML) | YAML (serde_yaml) | YAML (js-yaml) |
| Testing | `go test` | pytest | `cargo test` | Vitest |
| Linting | golangci-lint | ruff | clippy | Biome |
| Type checking | Built-in | mypy | Built-in (strict) | `tsc` (strict) |
| Build system | `go build` | `python -m build` | `cargo build` | `tsc` |
| Package registry | pkg.go.dev | PyPI | crates.io | npm |
| Cross-compilation | `GOOS`/`GOARCH` | PyInstaller | `cargo-dist` | `pkg`/`nexe` |
| Version injection | ldflags | `__version__` variable | `CARGO_PKG_VERSION` | `package.json` version |
| Config dir | `~/.config/<name>/` | `~/.config/<name>/` | `~/.config/<name>/` | `~/.config/<name>/` |

## Agent Prompt Template

When an agent receives a request, it should evaluate:

1. **What does the CLI do?** (data processing, API wrapper, system tool, etc.)
2. **Who are the users?** (developers, data scientists, ops, end users)
3. **How will it be distributed?** (binary, pip, crates.io, internal)
4. **What are performance requirements?** (latency, throughput, memory)
5. **What ecosystem does it need?** (cloud APIs, ML libs, system calls)

Then read this guide and pick the best fit.
