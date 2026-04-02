use std::io::Write;
use std::process::{Command, Stdio};

/// Abstracts command execution for testability.
pub trait CommandExecutor {
    /// Executes a command and returns combined stdout output.
    fn run(&self, program: &str, args: &[&str]) -> anyhow::Result<String>;

    /// Executes a command with stdin and returns stdout.
    fn run_with_stdin(&self, program: &str, args: &[&str], stdin: &str) -> anyhow::Result<String>;
}

/// Shells out to real commands.
pub struct RealExecutor;

impl CommandExecutor for RealExecutor {
    fn run(&self, program: &str, args: &[&str]) -> anyhow::Result<String> {
        let output = Command::new(program)
            .args(args)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .output()
            .map_err(|e| anyhow::anyhow!("{e}"))?;

        if !output.status.success() {
            let stderr = String::from_utf8_lossy(&output.stderr);
            anyhow::bail!("{}: {stderr}", output.status);
        }

        Ok(String::from_utf8_lossy(&output.stdout).into_owned())
    }

    fn run_with_stdin(&self, program: &str, args: &[&str], stdin: &str) -> anyhow::Result<String> {
        let mut child = Command::new(program)
            .args(args)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .map_err(|e| anyhow::anyhow!("{e}"))?;

        if let Some(mut child_stdin) = child.stdin.take() {
            child_stdin.write_all(stdin.as_bytes())?;
        }

        let output = child.wait_with_output()?;

        if !output.status.success() {
            let stderr = String::from_utf8_lossy(&output.stderr);
            anyhow::bail!("{}: {stderr}", output.status);
        }

        Ok(String::from_utf8_lossy(&output.stdout).into_owned())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_real_executor_run() {
        let exec = RealExecutor;
        let out = exec.run("echo", &["hello"]).unwrap();
        assert!(out.contains("hello"));
    }

    #[test]
    fn test_real_executor_run_error() {
        let exec = RealExecutor;
        let result = exec.run("nonexistent-command-abc123", &[]);
        assert!(result.is_err());
    }

    #[test]
    fn test_real_executor_run_with_stdin() {
        let exec = RealExecutor;
        let out = exec.run_with_stdin("cat", &[], "hello from stdin").unwrap();
        assert!(out.contains("hello from stdin"));
    }
}
