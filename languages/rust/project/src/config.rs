use std::fs;
use std::path::{Path, PathBuf};

use serde::{Deserialize, Serialize};

/// Top-level configuration.
///
/// Add your project-specific config fields here.
/// Example:
///   default_agent: Option<String>,
///   agents: Option<std::collections::HashMap<String, AgentConfig>>,
#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq)]
pub struct Config {}

/// Returns the configuration directory path.
///
/// Uses `~/.config/__PROJECT_NAME__/`.
pub fn config_dir() -> anyhow::Result<PathBuf> {
    let home = dirs::home_dir()
        .ok_or_else(|| anyhow::anyhow!("unable to determine home directory"))?;
    Ok(home.join(".config").join("__PROJECT_NAME__"))
}

/// Returns the full path to the config file.
pub fn config_path() -> anyhow::Result<PathBuf> {
    Ok(config_dir()?.join("config.yaml"))
}

/// Loads config from the default path, falling back to defaults if no file exists.
pub fn load() -> anyhow::Result<Config> {
    load_from(&config_path()?)
}

/// Loads config from a specific path, falling back to defaults if no file exists.
pub fn load_from(path: &Path) -> anyhow::Result<Config> {
    match fs::read_to_string(path) {
        Ok(contents) => {
            let cfg: Config = serde_yaml::from_str(&contents)
                .map_err(|e| anyhow::anyhow!("parsing config {}: {}", path.display(), e))?;
            Ok(cfg)
        }
        Err(err) if err.kind() == std::io::ErrorKind::NotFound => Ok(Config::default()),
        Err(err) => Err(anyhow::anyhow!("reading config: {err}")),
    }
}

/// Saves config to the default path, creating directories as needed.
pub fn save(cfg: &Config) -> anyhow::Result<()> {
    save_to(cfg, &config_path()?)
}

/// Saves config to a specific path, creating directories as needed.
pub fn save_to(cfg: &Config, path: &Path) -> anyhow::Result<()> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)
            .map_err(|e| anyhow::anyhow!("creating config directory: {e}"))?;
    }

    let contents = serde_yaml::to_string(cfg)
        .map_err(|e| anyhow::anyhow!("marshaling config: {e}"))?;

    fs::write(path, contents)
        .map_err(|e| anyhow::anyhow!("writing config: {e}"))?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn test_default_config() {
        let cfg = Config::default();
        // Default config should be valid.
        let _ = cfg;
    }

    #[test]
    fn test_config_dir() {
        let dir = config_dir().unwrap();
        assert!(dir.ends_with(".config/__PROJECT_NAME__"));
    }

    #[test]
    fn test_config_path() {
        let path = config_path().unwrap();
        assert!(path.ends_with("config.yaml"));
        assert!(path
            .to_string_lossy()
            .contains(".config/__PROJECT_NAME__"));
    }

    #[test]
    fn test_load_no_file() {
        let tmp = TempDir::new().unwrap();
        let path = tmp.path().join("nonexistent/config.yaml");
        let cfg = load_from(&path).unwrap();
        assert_eq!(cfg, Config::default());
    }

    #[test]
    fn test_save_and_load() {
        let tmp = TempDir::new().unwrap();
        let path = tmp.path().join("config.yaml");

        let cfg = Config::default();
        save_to(&cfg, &path).unwrap();

        let loaded = load_from(&path).unwrap();
        assert_eq!(loaded, cfg);
    }

    #[test]
    fn test_save_creates_directories() {
        let tmp = TempDir::new().unwrap();
        let path = tmp.path().join("nested/deep/config.yaml");

        let cfg = Config::default();
        save_to(&cfg, &path).unwrap();

        assert!(path.exists());
    }

    #[test]
    fn test_load_invalid_yaml() {
        let tmp = TempDir::new().unwrap();
        let path = tmp.path().join("bad.yaml");
        fs::write(&path, "{{invalid yaml").unwrap();

        let result = load_from(&path);
        assert!(result.is_err());
    }
}
