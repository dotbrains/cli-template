import { Command } from "commander";
import { defaultConfig, saveConfig, configPath } from "./config.js";
import { homedir } from "node:os";
import { relative } from "node:path";

const VERSION = "0.1.0";

const program = new Command();

program
  .name("__PROJECT_NAME__")
  .description("__PROJECT_DESCRIPTION_LONG__")
  .version(VERSION);

const configCmd = program.command("config").description("Manage configuration");

configCmd
  .command("init")
  .description("Create default config file")
  .option("--force", "Overwrite existing config")
  .action(async (opts: { force?: boolean }) => {
    const cfgPath = configPath();

    if (!opts.force) {
      const { existsSync } = await import("node:fs");
      if (existsSync(cfgPath)) {
        console.error(
          `Error: config already exists at ${cfgPath} (use --force to overwrite)`,
        );
        process.exit(1);
      }
    }

    saveConfig(defaultConfig());

    const home = homedir();
    const display = cfgPath.startsWith(home)
      ? `~/${relative(home, cfgPath)}`
      : cfgPath;

    console.log(`✓ Wrote default config to ${display}`);
    console.log("Edit the file to customize settings.");
  });

export function main(): void {
  program.parse();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
