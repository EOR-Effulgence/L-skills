# AGENTS.md

L-skills の知見集（Codex / GitHub Copilot CLI 用、自動生成）

## 一覧

- **cadquery-bit-case**: build123d でドライバービット収納ケースを生成する。1/4 hex / 4mm 精密ビット 等のグリッド配置ケース＋スナップフィット蓋を STL/STEP 出力
- **python-patterns**: Python プロジェクトのベストプラクティスとパターン集（uv / pydantic / pytest / イミュータブル）
- **rust-patterns**: Rust プロジェクトのベストプラクティスとパターン集（cargo workspace / clippy / thiserror / anyhow）
- **typescript-patterns**: TypeScript プロジェクトのベストプラクティスとパターン集（mise / strict tsconfig / zod / monorepo）

---

## cadquery-bit-case

# Bit Case Generator (build123d)

ドライバービット収納ケースをパラメトリックに生成するスキル。
本体（グリッド穴）+ スナップフィット蓋 の2パーツ構成。

## デフォルト仕様（標準）

| 項目 | 値 |
|---|---|
| ビット規格 | 1/4 インチ六角軸 (対角 7.0mm) |
| ビット長 | 65mm |
| 穴径 | Φ7.2mm（クリアランス +0.2mm） |
| 穴深さ | 55mm（10mm 突き出し） |
| グリッド | 4列 × 5行 = 20本 |
| ピッチ | 13mm |
| 外形 | 約 70 × 84 × 60mm |
| 蓋 | スナップフィット（4辺リップ） |
| 推奨フィラメント | PLA（本体）+ PLA別色（蓋）→ AMS Lite で2色 |

## 使い方

### 必要環境

```bash
# uv で依存を入れる（pip 不要）
cd ~/Documents/L-skills/skills/cadquery-bit-case
uv venv
uv pip install build123d
```

### 生成

```bash
uv run python generate.py
```

`output/` に以下が生成される:

- `bit_case_base.stl` — 本体（穴あきグリッド）
- `bit_case_lid.stl`  — 蓋（スナップ）
- `bit_case_assembly.step` — 組立確認用 STEP

### Bambu Studio で印刷

1. 両 STL を読み込み
2. **本体**: 穴を上に向けて配置（サポート不要）
3. **蓋**: 内側を上に向けて配置（サポート不要）
4. PLA 0.2mm レイヤー、infill 20%
5. AMS Lite で本体/蓋を別色割当

## カスタマイズ

`generate.py` 冒頭の定数を書き換えて再実行:

```python
COLS, ROWS = 4, 5         # 列×行
BIT_LENGTH = 65           # ビット長 (mm)
HOLE_DEPTH = 55           # 穴深さ (mm)
HOLE_DIAMETER = 7.2       # 穴径 (mm) クリアランス込
PITCH = 13                # 穴中心間距離 (mm)
```

### よくある変更例

| 用途 | 変更 |
|---|---|
| 4mm精密ビット (時計工具) | `HOLE_DIAMETER = 4.2`, `BIT_LENGTH = 28`, `HOLE_DEPTH = 22`, `PITCH = 8` |
| 50mm 標準ビット | `BIT_LENGTH = 50`, `HOLE_DEPTH = 40` |
| 30本収納 (5×6) | `COLS, ROWS = 5, 6` |
| 携帯ポケット版 | `PITCH = 11`（密集配置） |

## 設計メモ

- **クリアランス +0.2mm**: A1 mini + PLA で実測 fit する値。きついなら +0.3mm に
- **蓋リップ高さ 5mm**: スナップフィットの保持力。低いと外れる、高いとはまらない
- **底厚 4mm**: 落下耐性。携帯用は 5mm 推奨
- **印刷向き**: 本体は穴を上、蓋は内側を上 → サポート完全不要

## トラブルシュート

| 症状 | 対処 |
|---|---|
| 蓋がきつくて閉まらない | `LID_INNER_GAP = 0.3` → `0.4` |
| 蓋がゆるい | `LID_INNER_GAP = 0.3` → `0.2` |
| ビットがきつい | `HOLE_DIAMETER` を +0.1mm |
| ビットが抜けやすい | `HOLE_DIAMETER` を -0.1mm、または底に磁石用ザグリ追加 |

---

## python-patterns

# Python パターン

## uv でのプロジェクト管理

```bash
uv init my-project
cd my-project
uv add fastapi pydantic
uv add --dev pytest pytest-cov ruff mypy
uv run python main.py
uv run pytest
```

## pyproject.toml 構成

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "pydantic>=2.0"]

[dependency-groups]
dev = ["pytest>=8.0", "pytest-cov>=5.0", "ruff>=0.8", "mypy>=1.13"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "TCH"]

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"
```

## pydantic バリデーション

```python
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    """イミュータブルなユーザーモデル"""
    model_config = {"frozen": True}

    name: str = Field(min_length=1)
    email: EmailStr
    age: int | None = Field(default=None, gt=0)

user = User(name="田中", email="tanaka@example.com")
updated = user.model_copy(update={"name": "佐藤"})
```

## テストパターン (pytest)

```python
import pytest
from my_project.models import User

class TestUser:
    def test_正常系_ユーザー作成(self):
        user = User(name="テスト", email="test@example.com")
        assert user.name == "テスト"

    def test_異常系_空の名前(self):
        with pytest.raises(ValueError):
            User(name="", email="test@example.com")

@pytest.fixture
def sample_user() -> User:
    return User(name="テスト", email="test@example.com")

@pytest.mark.parametrize("name,valid", [
    ("valid", True),
    ("", False),
])
def test_名前バリデーション(name: str, valid: bool):
    if valid:
        User(name=name, email="t@e.com")
    else:
        with pytest.raises(ValueError):
            User(name=name, email="t@e.com")
```

## イミュータブルパターン

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Config:
    host: str = "localhost"
    port: int = 8080

config = Config()
updated = replace(config, port=3000)
```

---

## rust-patterns

# Rust パターン

## cargo workspace 構成

```toml
# Cargo.toml (ルート)
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
```

```toml
# crates/my-lib/Cargo.toml
[dependencies]
serde = { workspace = true }
```

## clippy / rustfmt 設定

```toml
# clippy.toml
cognitive-complexity-threshold = 10

# rustfmt.toml
edition = "2021"
max_width = 100
use_field_init_shorthand = true
```

- `cargo clippy -- -W clippy::pedantic` で厳格チェック
- `cargo fmt --check` で CI チェック

## エラーハンドリング

```rust
// ライブラリ: thiserror で型安全なエラー定義
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("設定ファイルが見つかりません: {path}")]
    ConfigNotFound { path: String },
    #[error("IO エラー")]
    Io(#[from] std::io::Error),
}

// アプリケーション: anyhow で簡潔なエラー伝播
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context("設定ファイルの読み込みに失敗")?;
    toml::from_str(&content)
        .context("設定ファイルのパースに失敗")
}
```

## テストパターン

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_正常系() {
        let result = process_input("valid");
        assert!(result.is_ok());
    }

    #[test]
    fn test_異常系_空入力() {
        let result = process_input("");
        assert!(matches!(result, Err(AppError::InvalidInput { .. })));
    }
}
```

## イミュータブルパターン

```rust
fn update_name(user: &User, name: String) -> User {
    User { name, ..user.clone() }
}

let config = ConfigBuilder::new()
    .port(8080)
    .host("localhost")
    .build()?;
```

---

## typescript-patterns

# TypeScript パターン

## mise でのバージョン管理

```toml
# .mise.toml
[tools]
node = "lts"

[env]
NODE_ENV = "development"
```

- `mise install` でバージョン固定
- `.mise.toml` をリポジトリにコミット

## tsconfig.json 推奨設定

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "isolatedModules": true,
    "moduleResolution": "bundler",
    "target": "ES2022",
    "module": "ES2022"
  }
}
```

## zod バリデーションパターン

```typescript
import { z } from "zod";

const UserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

type User = z.infer<typeof UserSchema>;

const parseUser = (input: unknown): User => UserSchema.parse(input);
```

## イミュータブルパターン

```typescript
const addItem = <T>(items: readonly T[], item: T): readonly T[] => [...items, item];
const removeAt = <T>(items: readonly T[], index: number): readonly T[] =>
  items.filter((_, i) => i !== index);

const updateUser = (user: Readonly<User>, patch: Partial<User>): User => ({
  ...user,
  ...patch,
});
```

## monorepo パターン (npm workspaces)

```json
{
  "workspaces": ["packages/*", "apps/*"]
}
```

- 共有型は `packages/shared-types/` に配置
- 各パッケージは独立した `tsconfig.json` を持つ
- `tsconfig.base.json` で共通設定を管理
