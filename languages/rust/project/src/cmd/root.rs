use clap::{Parser, Subcommand};

/// __PROJECT_DESCRIPTION_LONG__
#[derive(Parser, Debug)]
#[command(
    name = "__PROJECT_NAME__",
    about = "__PROJECT_DESCRIPTION__",
    version,
    disable_help_subcommand = true,
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand, Debug)]
pub enum Commands {
    /// Manage configuration
    Config {
        #[command(subcommand)]
        command: ConfigCommands,
    },
}

#[derive(Subcommand, Debug)]
pub enum ConfigCommands {
    /// Create default config file
    Init {
        /// Overwrite existing config
        #[arg(long)]
        force: bool,
    },
}

impl Cli {
    /// Parse CLI arguments with the given version string.
    pub fn parse(version: &str) -> Self {
        use clap::CommandFactory;

        let mut cli = <Self as CommandFactory>::command().version(version);
        let matches = cli.get_matches_mut();
        <Self as clap::FromArgMatches>::from_arg_matches(&matches)
            .map_err(|e| e.exit())
            .unwrap()
    }
}
