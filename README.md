# L-skills

EOR-Effulgence の個人用スキル・コマンド・エージェント集。
**Claude Code をネイティブ対応**としつつ、Codex / Cursor / Gemini CLI でも同じ知見を流用できる構成。

## 構成

```
L-skills/
├── .claude-plugin/plugin.json   # Claude Code plugin manifest
├── marketplace.json             # Claude Code marketplace 登録用
├── skills/                      # 一次ソース（Markdown + frontmatter）
│   └── <skill-name>/SKILL.md
├── commands/                    # スラッシュコマンド（Claude Code）
├── agents/                      # サブエージェント定義
├── AGENTS.md                    # Codex / Copilot CLI 用（自動生成）
├── GEMINI.md                    # Gemini CLI 用（自動生成）
├── .cursor/rules/               # Cursor 用（自動生成）
└── scripts/sync.ts              # skills/ → 各ツール形式に変換
```

## 使い方

### Claude Code（ネイティブ）

```bash
# ローカル開発
claude --plugin-dir ~/Documents/L-skills

# marketplace 経由 install
/plugin marketplace add EOR-Effulgence/L-skills
/plugin install l-skills
```

呼び出し: `/l-skills:<skill-name>`

### Codex / GitHub Copilot CLI

`AGENTS.md` をプロジェクトに symlink するか、L-skills 内で実行する。

```bash
ln -s ~/Documents/L-skills/AGENTS.md ./AGENTS.md
```

### Cursor

`.cursor/rules/` をプロジェクトに symlink する。

```bash
ln -s ~/Documents/L-skills/.cursor/rules ./.cursor/rules
```

### Gemini CLI

`GEMINI.md` を `~/.gemini/` 配下に配置するか symlink。

## スキル追加フロー

1. `skills/<name>/SKILL.md` を作成（frontmatter 必須: name, description）
2. `pnpm sync`（または `node scripts/sync.ts`）で AGENTS.md / GEMINI.md / .cursor/rules を再生成
3. commit & push

## 同期スクリプト

`scripts/sync.ts` が `skills/*/SKILL.md` を一次ソースとして:

- `AGENTS.md` に concat（Codex/Copilot CLI）
- `.cursor/rules/<name>.mdc` に変換コピー
- `GEMINI.md` にマージ

## ライセンス

MIT
