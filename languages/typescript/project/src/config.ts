import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { homedir } from "node:os";
import yaml from "js-yaml";

/**
 * Top-level configuration.
 *
 * Add your project-specific config fields here.
 *
 * Example:
 *   defaultAgent?: string;
 *   agents?: Record<string, AgentConfig>;
 */
export interface Config {
  // Add your project-specific config fields here.
}

/** Returns the built-in default configuration. */
export function defaultConfig(): Config {
  return {};
}

/** Returns the configuration directory path. */
export function configDir(): string {
  return join(homedir(), ".config", "__PROJECT_NAME__");
}

/** Returns the full path to the config file. */
export function configPath(): string {
  return join(configDir(), "config.yaml");
}

/**
 * Reads config from disk, falling back to defaults if no file exists.
 */
export function loadConfig(path?: string): Config {
  const filePath = path ?? configPath();

  if (!existsSync(filePath)) {
    return defaultConfig();
  }

  try {
    const content = readFileSync(filePath, "utf-8");
    const raw = yaml.load(content) as Record<string, unknown> | null;
    return { ...defaultConfig(), ...raw } as Config;
  } catch (err) {
    if (err instanceof yaml.YAMLException) {
      throw new Error(`parsing config ${filePath}: ${err.message}`);
    }
    throw new Error(`reading config: ${err}`);
  }
}

/**
 * Writes config to disk, creating directories as needed.
 */
export function saveConfig(cfg: Config, path?: string): void {
  const filePath = path ?? configPath();
  const dir = dirname(filePath);

  mkdirSync(dir, { recursive: true });

  const content = yaml.dump(cfg, { sortKeys: false });
  writeFileSync(filePath, content, "utf-8");
}
