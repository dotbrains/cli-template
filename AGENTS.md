# Agent Instructions for cli-template

This repo scaffolds production-ready CLI projects in Go, Python, or Rust.

## When to Use This

Use this repo when the user asks to create a CLI tool, command-line application, or terminal utility. Examples:
- "Create a CLI called filesum that computes file checksums"
- "Build me a tool that converts JSON to YAML"
- "I need a command-line app for managing SSH keys"

## How to Use

### Step 1: Read LANGUAGES.md

Read `~/Documents/GitHub/github.com/dotbrains/cli-template/LANGUAGES.md` to decide which language fits best.

Decision shortcuts:
- **Performance-critical, simple I/O, single binary needed** → Rust
- **API wrappers, DevOps tools, cloud integrations** → Go
- **Data processing, rapid prototyping, wraps Python libraries** → Python
- **User didn't specify and no strong reason** → Go (best balance)

### Step 2: Run generate.sh

```bash
cd ~/Documents/GitHub/github.com/dotbrains/cli-template
./generate.sh \
  --lang <go|python|rust> \
  --name <project-name> \
  --desc "<one-line description>" \
  --desc-long "<1-2 sentence description>"
```

This creates `output/<project-name>/` with all files scaffolded.

### Step 3: Move the project to the user's workspace

```bash
mv ~/Documents/GitHub/github.com/dotbrains/cli-template/output/<project-name> \
   ~/Documents/GitHub/github.com/dotbrains/<project-name>
```

### Step 4: Initialize and verify

```bash
cd ~/Documents/GitHub/github.com/dotbrains/<project-name>
git init && git add -A && git commit -m "chore: scaffold from cli-template"

# For Go only:
rm go.mod go.sum && go mod init github.com/dotbrains/<project-name> && go mod tidy

# For all:
make build && make test
```

### Step 5: Customize

After scaffolding, customize the project for the user's specific needs:
1. Add project-specific config fields to the config module
2. Add subcommands for the CLI's actual functionality
3. Implement domain logic
4. Update README.md, SPEC.md with real descriptions
5. Replace placeholder content

## Manifest Files

Each language has a `manifest.json` with metadata the agent can read:
- `install_cmd` — how users install the tool
- `build_cmd` — how to build
- `test_cmd` — how to run tests
- `framework` — the CLI framework used

Read `languages/<lang>/manifest.json` for these details.
