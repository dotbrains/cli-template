mod cmd;
mod config;
mod exec;

/// Version injected at build time via `CARGO_PKG_VERSION` or `-ldflags` equivalent.
/// Override at build: `VERSION=1.2.3 cargo build`
const VERSION: &str = match option_env!("VERSION") {
    Some(v) => v,
    None => env!("CARGO_PKG_VERSION"),
};

fn main() {
    if let Err(err) = cmd::execute(VERSION) {
        eprintln!("error: {err}");
        std::process::exit(1);
    }
}
