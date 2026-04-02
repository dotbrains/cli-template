# cli-template — Multi-Language CLI Scaffold

[![License: PolyForm Shield 1.0.0](https://img.shields.io/badge/License-PolyForm%20Shield%201.0.0-blue.svg)](https://polyformproject.org/licenses/shield/1.0.0/)

![Go](https://img.shields.io/badge/-Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Rust](https://img.shields.io/badge/-Rust-DEA584?style=flat-square&logo=rust&logoColor=white)
![macOS](https://img.shields.io/badge/-macOS-000000?style=flat-square&logo=apple&logoColor=white)
![Linux](https://img.shields.io/badge/-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)

One repo, three languages. Tell an agent what CLI you need — it picks Go, Python, or Rust and scaffolds a production-ready project.

## Quick Start

```sh
# Clone the template
git clone https://github.com/dotbrains/cli-template.git
cd cli-template

# Scaffold a Go project
./generate.sh --lang go --name my-tool --desc "My CLI tool" --desc-long "Does something useful."

# Scaffold a Python project
./generate.sh --lang python --name my-tool --desc "My CLI tool" --desc-long "Does something useful."

# Scaffold a Rust project
./generate.sh --lang rust --name my-tool --desc "My CLI tool" --desc-long "Does something useful."

# Build and test
cd output/my-tool
make build
make test
```

## How It Works

```
User: "Build me a fast file checksum CLI"
Agent reads: LANGUAGES.md → Rust wins (performance-critical)
Agent runs:  ./generate.sh --lang rust --name filesum --desc "..." --desc-long "..."
Output:      output/filesum/ — ready to develop
```

The generator:
1. Copies shared files (LICENSE, website/, assets/) to the output
2. Copies language-specific source code and build config
3. Renders documentation templates — keeps the chosen language's sections, removes the others
4. Replaces `__PROJECT_NAME__` placeholders everywhere

## Structure

```
cli-template/
├── LANGUAGES.md                 # Decision guide for choosing a language
├── generate.sh                  # Scaffold script
├── shared/                      # Files identical across all languages
│   ├── LICENSE                  # PolyForm Shield 1.0.0
│   ├── .gitignore.common        # Shared gitignore patterns
│   ├── assets/.gitkeep
│   └── website/                 # Next.js + Tailwind marketing site
├── templates/                   # Docs with {{#go}}...{{/go}} blocks
│   ├── README.md.tmpl
│   ├── SPEC.md.tmpl
│   └── TEMPLATE.md.tmpl
└── languages/
    ├── go/
    │   ├── manifest.json        # Metadata: install cmd, badges, deps
    │   ├── project/             # Maps to output root
    │   │   ├── main.go
    │   │   ├── cmd/
    │   │   └── internal/
    │   ├── overlays/            # .gitignore, Makefile, workflows, linter
    │   ├── go.mod, go.sum
    ├── python/
    │   ├── manifest.json
    │   ├── project/
    │   │   ├── src/__PROJECT_NAME__/
    │   │   └── tests/
    │   ├── overlays/
    │   └── pyproject.toml
    └── rust/
        ├── manifest.json
        ├── project/
        │   ├── src/
        │   └── tests/
        ├── overlays/
        ├── Cargo.toml
        └── rust-toolchain.toml
```

## Choosing a Language

| Factor | Go | Python | Rust |
|---|---|---|---|
| Cold start | Fast | Slow | Instant |
| Binary size | ~10MB | Needs Python | ~2MB |
| Distribution | Single binary | pip | Single binary |
| Prototyping speed | Good | Best | Slowest |
| Performance | Great | Adequate | Best |

**Go** — DevOps tools, API wrappers, anything that needs `go install`. Best balance of productivity and performance.

**Python** — Data pipelines, wrappers around Python libraries, internal tools where startup time doesn't matter.

**Rust** — System utilities, file processors, security tools, CI/CD speed-critical CLIs.

See [LANGUAGES.md](LANGUAGES.md) for the full decision guide and flowchart.

## What Each Project Gets

Every generated project includes:

- **CLI framework** — Cobra (Go), Click (Python), or Clap (Rust)
- **YAML config** — Load/save defaults at `~/.config/<name>/config.yaml`
- **Command executor** — Abstracted shell execution for testability
- **Tests** — Unit + integration tests with 80%+ coverage target
- **CI/CD** — GitHub Actions for test, lint, build, and release
- **Makefile** — `build`, `test`, `lint`, `install`, `clean`
- **Marketing site** — Next.js + Tailwind website (shared)
- **Documentation** — README, SPEC, and TEMPLATE.md

## Adding a Language

1. Create `languages/<name>/` with:
   - `project/` — source files that map to the output root
   - `overlays/` — `.gitignore`, `Makefile`, workflows, linter configs
   - `manifest.json` — install/build/test commands, badge metadata
2. Add `{{#<name>}}...{{/<name>}}` blocks to `templates/*.tmpl`
3. Add a section to `LANGUAGES.md`

## Dependencies

None beyond `bash`, `rsync`, `perl`, and `sed` (all pre-installed on macOS/Linux).

## License

This project is licensed under the [PolyForm Shield License 1.0.0](https://polyformproject.org/licenses/shield/1.0.0/) — see [LICENSE](shared/LICENSE) for details.
