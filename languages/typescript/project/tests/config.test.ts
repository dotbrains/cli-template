import { describe, it, expect, beforeEach } from "vitest";
import { join } from "node:path";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import {
  defaultConfig,
  configDir,
  configPath,
  loadConfig,
  saveConfig,
} from "../src/config.js";

describe("Config", () => {
  it("defaultConfig returns an object", () => {
    const cfg = defaultConfig();
    expect(cfg).toBeDefined();
    expect(typeof cfg).toBe("object");
  });

  it("configDir returns expected path", () => {
    const dir = configDir();
    expect(dir).toContain(".config/__PROJECT_NAME__");
  });

  it("configPath returns expected path", () => {
    const path = configPath();
    expect(path).toContain("config.yaml");
    expect(path).toContain(".config/__PROJECT_NAME__");
  });

  describe("loadConfig", () => {
    it("returns defaults when no file exists", () => {
      const cfg = loadConfig("/nonexistent/path/config.yaml");
      expect(cfg).toBeDefined();
    });

    it("loads config from file", () => {
      const dir = join(tmpdir(), `__PROJECT_NAME__-config-test-${Date.now()}`);
      mkdirSync(dir, { recursive: true });
      const path = join(dir, "config.yaml");
      writeFileSync(path, "# empty config\n");
      try {
        const cfg = loadConfig(path);
        expect(cfg).toBeDefined();
      } finally {
        rmSync(dir, { recursive: true, force: true });
      }
    });

    it("throws on invalid YAML", () => {
      const dir = join(tmpdir(), `__PROJECT_NAME__-config-test-${Date.now()}`);
      mkdirSync(dir, { recursive: true });
      const path = join(dir, "bad.yaml");
      writeFileSync(path, "{{invalid yaml");
      try {
        expect(() => loadConfig(path)).toThrow("parsing config");
      } finally {
        rmSync(dir, { recursive: true, force: true });
      }
    });
  });

  describe("saveConfig", () => {
    it("creates config file and directories", () => {
      const dir = join(tmpdir(), `__PROJECT_NAME__-config-test-${Date.now()}`);
      const path = join(dir, "nested", "config.yaml");
      try {
        saveConfig(defaultConfig(), path);
        expect(
          (() => {
            try {
              return require("node:fs").existsSync(path);
            } catch {
              return false;
            }
          })(),
        ).toBe(true);
      } finally {
        rmSync(dir, { recursive: true, force: true });
      }
    });

    it("round-trips config", () => {
      const dir = join(tmpdir(), `__PROJECT_NAME__-config-test-${Date.now()}`);
      const path = join(dir, "config.yaml");
      try {
        saveConfig(defaultConfig(), path);
        const loaded = loadConfig(path);
        expect(loaded).toBeDefined();
      } finally {
        rmSync(dir, { recursive: true, force: true });
      }
    });
  });
});
