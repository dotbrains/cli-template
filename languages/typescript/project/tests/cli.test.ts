import { describe, it, expect } from "vitest";
import { execFileSync } from "node:child_process";
import { join } from "node:path";
import { existsSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";

const BIN = join(import.meta.dirname, "../src/cli.ts");
const RUN = (args: string[], env?: Record<string, string>) =>
  execFileSync("npx", ["tsx", BIN, ...args], {
    encoding: "utf-8",
    env: { ...process.env, ...env },
  });

describe("__PROJECT_NAME__ CLI", () => {
  it("shows version", () => {
    const out = RUN(["--version"]);
    expect(out).toContain("0.1.0");
  });

  it("shows help", () => {
    const out = RUN(["--help"]);
    expect(out).toContain("__PROJECT_NAME__");
    expect(out).toContain("config");
  });

  describe("config init", () => {
    it("creates config file", () => {
      const home = join(tmpdir(), `__PROJECT_NAME__-test-${Date.now()}`);
      mkdirSync(home, { recursive: true });
      try {
        const out = RUN(["config", "init"], { HOME: home });
        expect(out).toContain("Wrote default config");

        const cfgPath = join(home, ".config", "__PROJECT_NAME__", "config.yaml");
        expect(existsSync(cfgPath)).toBe(true);
      } finally {
        rmSync(home, { recursive: true, force: true });
      }
    });

    it("fails when config exists", () => {
      const home = join(tmpdir(), `__PROJECT_NAME__-test-${Date.now()}`);
      const cfgDir = join(home, ".config", "__PROJECT_NAME__");
      mkdirSync(cfgDir, { recursive: true });
      writeFileSync(join(cfgDir, "config.yaml"), "existing");
      try {
        expect(() => RUN(["config", "init"], { HOME: home })).toThrow();
      } finally {
        rmSync(home, { recursive: true, force: true });
      }
    });

    it("overwrites with --force", () => {
      const home = join(tmpdir(), `__PROJECT_NAME__-test-${Date.now()}`);
      const cfgDir = join(home, ".config", "__PROJECT_NAME__");
      mkdirSync(cfgDir, { recursive: true });
      writeFileSync(join(cfgDir, "config.yaml"), "existing");
      try {
        const out = RUN(["config", "init", "--force"], { HOME: home });
        expect(out).toContain("Wrote default config");
      } finally {
        rmSync(home, { recursive: true, force: true });
      }
    });
  });
});
