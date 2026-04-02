import { execFileSync } from "node:child_process";

/**
 * Abstracts command execution for testability.
 */
export interface CommandExecutor {
  /** Executes a command and returns stdout. */
  run(program: string, args: string[], timeout?: number): string;

  /** Executes a command with stdin and returns stdout. */
  runWithStdin(
    program: string,
    args: string[],
    stdin: string,
    timeout?: number,
  ): string;
}

/** Shells out to real commands. */
export class RealExecutor implements CommandExecutor {
  run(program: string, args: string[], timeout?: number): string {
    return execFileSync(program, args, {
      encoding: "utf-8",
      timeout: timeout ?? 30_000,
    });
  }

  runWithStdin(
    program: string,
    args: string[],
    stdin: string,
    timeout?: number,
  ): string {
    return execFileSync(program, args, {
      input: stdin,
      encoding: "utf-8",
      timeout: timeout ?? 30_000,
    });
  }
}

/** Mock executor for testing. Use callbacks to control behavior. */
export class MockExecutor implements CommandExecutor {
  constructor(
    private runFunc?: (program: string, ...args: string[]) => string,
    private runWithStdinFunc?: (
      program: string,
      args: string[],
      stdin: string,
    ) => string,
  ) {}

  run(program: string, args: string[]): string {
    if (this.runFunc) {
      return this.runFunc(program, ...args);
    }
    return "";
  }

  runWithStdin(program: string, args: string[], stdin: string): string {
    if (this.runWithStdinFunc) {
      return this.runWithStdinFunc(program, args, stdin);
    }
    return "";
  }
}
