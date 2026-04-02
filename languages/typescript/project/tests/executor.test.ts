import { describe, it, expect } from "vitest";
import { RealExecutor, MockExecutor } from "../src/executor.js";

describe("RealExecutor", () => {
  it("runs a command and captures stdout", () => {
    const exec = new RealExecutor();
    const out = exec.run("echo", ["hello"]);
    expect(out.trim()).toBe("hello");
  });

  it("throws on nonexistent command", () => {
    const exec = new RealExecutor();
    expect(() => exec.run("nonexistent-command-abc123", [])).toThrow();
  });

  it("runs with stdin", () => {
    const exec = new RealExecutor();
    const out = exec.runWithStdin("cat", [], "hello from stdin");
    expect(out).toContain("hello from stdin");
  });
});

describe("MockExecutor", () => {
  it("uses provided callback", () => {
    const mock = new MockExecutor(() => "mocked output");
    const out = mock.run("anything", []);
    expect(out).toBe("mocked output");
  });

  it("returns empty string by default", () => {
    const mock = new MockExecutor();
    expect(mock.run("anything", [])).toBe("");
    expect(mock.runWithStdin("anything", [], "stdin")).toBe("");
  });
});
