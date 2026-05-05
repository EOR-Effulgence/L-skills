#!/usr/bin/env node
/**
 * skills/*\/SKILL.md を一次ソースとして AGENTS.md / GEMINI.md / .cursor/rules を再生成する
 *
 * 使い方:
 *   pnpm tsx scripts/sync.ts
 */
import { readdir, readFile, writeFile, mkdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url)) + "/..";

interface Skill {
  readonly name: string;
  readonly description: string;
  readonly body: string;
  readonly raw: string;
}

const parseFrontmatter = (raw: string): Skill => {
  const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) throw new Error("frontmatter が見つかりません");
  const [, fm, body] = match;
  const name = fm.match(/^name:\s*(.+)$/m)?.[1]?.trim() ?? "";
  const description = fm.match(/^description:\s*(.+)$/m)?.[1]?.trim() ?? "";
  return { name, description, body: body.trim(), raw };
};

const loadSkills = async (): Promise<readonly Skill[]> => {
  const skillsDir = join(root, "skills");
  const entries = await readdir(skillsDir, { withFileTypes: true });
  const skills: Skill[] = [];
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const path = join(skillsDir, entry.name, "SKILL.md");
    const raw = await readFile(path, "utf8");
    skills.push(parseFrontmatter(raw));
  }
  return skills;
};

const buildAgentsMd = (skills: readonly Skill[]): string => {
  const header = `# AGENTS.md\n\nL-skills の知見集（Codex / GitHub Copilot CLI 用、自動生成）\n\n`;
  const toc = skills.map((s) => `- **${s.name}**: ${s.description}`).join("\n");
  const sections = skills.map((s) => `\n---\n\n## ${s.name}\n\n${s.body}`).join("\n");
  return `${header}## 一覧\n\n${toc}\n${sections}\n`;
};

const buildGeminiMd = (skills: readonly Skill[]): string =>
  buildAgentsMd(skills).replace(/^# AGENTS\.md/, "# GEMINI.md");

const writeCursorRules = async (skills: readonly Skill[]): Promise<void> => {
  const dir = join(root, ".cursor/rules");
  await mkdir(dir, { recursive: true });
  for (const skill of skills) {
    const content = `---\ndescription: ${skill.description}\n---\n\n${skill.body}\n`;
    await writeFile(join(dir, `${skill.name}.mdc`), content);
  }
};

const main = async (): Promise<void> => {
  const skills = await loadSkills();
  await writeFile(join(root, "AGENTS.md"), buildAgentsMd(skills));
  await writeFile(join(root, "GEMINI.md"), buildGeminiMd(skills));
  await writeCursorRules(skills);
  console.log(`synced ${skills.length} skills → AGENTS.md / GEMINI.md / .cursor/rules`);
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
