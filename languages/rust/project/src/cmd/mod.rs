pub mod root;

/// Entry point: parse CLI args and dispatch.
pub fn execute(version: &str) -> anyhow::Result<()> {
    let cli = root::Cli::parse(version);

    match cli.command {
        root::Commands::Config { command } => match command {
            root::ConfigCommands::Init { force } => {
                let cfg_path = crate::config::config_path()?;
                if !force && cfg_path.exists() {
                    anyhow::bail!(
                        "config already exists at {} (use --force to overwrite)",
                        cfg_path.display()
                    );
                }

                crate::config::save(&crate::config::Config::default())?;

                // Shorten the path for display.
                let display = match dirs::home_dir() {
                    Some(home) => match cfg_path.strip_prefix(&home) {
                        Ok(rel) => format!("~/{}", rel.display()),
                        Err(_) => cfg_path.display().to_string(),
                    },
                    None => cfg_path.display().to_string(),
                };

                println!("✓ Wrote default config to {display}");
                println!("Edit the file to customize settings.");
                Ok(())
            }
        },
    }
}
