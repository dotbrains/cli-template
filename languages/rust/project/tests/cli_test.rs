use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use tempfile::TempDir;

const BIN: &str = "__PROJECT_NAME__";

#[test]
fn test_version() {
    Command::cargo_bin(BIN)
        .unwrap()
        .arg("--version")
        .assert()
        .success()
        .stdout(predicate::str::contains("__PROJECT_NAME__"));
}

#[test]
fn test_help() {
    Command::cargo_bin(BIN)
        .unwrap()
        .arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("__PROJECT_NAME__"))
        .stdout(predicate::str::contains("config"));
}

#[test]
fn test_config_init() {
    let tmp = TempDir::new().unwrap();
    let home = tmp.path().display().to_string();

    Command::cargo_bin(BIN)
        .unwrap()
        .env("HOME", &home)
        .args(["config", "init"])
        .assert()
        .success()
        .stdout(predicate::str::contains("Wrote default config"));

    // Config file should exist.
    let config_path = tmp.path().join(".config/__PROJECT_NAME__/config.yaml");
    assert!(config_path.exists(), "config file not created");
}

#[test]
fn test_config_init_already_exists() {
    let tmp = TempDir::new().unwrap();
    let config_dir = tmp.path().join(".config/__PROJECT_NAME__");
    fs::create_dir_all(&config_dir).unwrap();
    fs::write(config_dir.join("config.yaml"), "existing").unwrap();

    let home = tmp.path().display().to_string();

    Command::cargo_bin(BIN)
        .unwrap()
        .env("HOME", &home)
        .args(["config", "init"])
        .assert()
        .failure()
        .stderr(predicate::str::contains("config already exists"));
}

#[test]
fn test_config_init_force() {
    let tmp = TempDir::new().unwrap();
    let config_dir = tmp.path().join(".config/__PROJECT_NAME__");
    fs::create_dir_all(&config_dir).unwrap();
    fs::write(config_dir.join("config.yaml"), "existing").unwrap();

    let home = tmp.path().display().to_string();

    Command::cargo_bin(BIN)
        .unwrap()
        .env("HOME", &home)
        .args(["config", "init", "--force"])
        .assert()
        .success()
        .stdout(predicate::str::contains("Wrote default config"));
}
