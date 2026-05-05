# GEMINI.md

L-skills の知見集（Codex / GitHub Copilot CLI 用、自動生成）

## 一覧

- **cadquery-bit-case**: build123d でドライバービット収納ケースを生成。横置き薄型タックルボックス型（U字溝＋ヘックス固定端、フラット蓋）
- **python-patterns**: Python プロジェクトのベストプラクティスとパターン集（uv / pydantic / pytest / イミュータブル）
- **rust-patterns**: Rust プロジェクトのベストプラクティスとパターン集（cargo workspace / clippy / thiserror / anyhow）
- **typescript-patterns**: TypeScript プロジェクトのベストプラクティスとパターン集（mise / strict tsconfig / zod / monorepo）

---

## cadquery-bit-case

# Bit Case Generator (build123d, 横置きB型)

ドライバービット収納ケースをパラメトリックに生成。
**横置き薄型** タックルボックス型 / U字チャネル + ヘックス固定端 / フラット蓋スナップフィット。

## デフォルト仕様

| 項目 | 値 |
|---|---|
| ビット規格 | 1/4 インチ六角軸 (対角 7.0mm) |
| ビット長 | 65mm |
| 本数 / 段数 | 15本 / 1段（並列横置き） |
| 溝径 | Φ7.2mm (クリアランス +0.2mm) |
| ピッチ | 10mm |
| ヘックス固定端 | 片側 10mm を +2mm 深掘り |
| 外形 | **162.2 × 80.0 × 7.6mm**（本体）/ 蓋 6mm |
| 合計厚 | 9.6mm（薄型） |
| 蓋 | 4辺リップでスナップ（被り 4mm、隙間 0.3mm） |
| 推奨フィラメント | PLA / PETG、AMS Lite で2色推奨 |

A1 mini 180×180mm ベッドに余裕で収まる。

## 構造

```
   ┌──────────────────────────────────────────┐ ← フラット蓋
   ├──────────────────────────────────────────┤
   │ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽       │ ← U字溝 ×15
   │ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎       │ ← ヘックス固定端（深溝）
   └──────────────────────────────────────────┘
        ↑ 65mm 沿いに横向きでビット配置
```

## 使い方

### セットアップ（初回のみ）

```bash
cd ~/Documents/L-skills/skills/cadquery-bit-case
uv venv --python 3.12
uv pip install build123d
```

### 生成

```bash
uv run python generate.py
```

`output/` に出力:
- `bit_case_base.stl` — 本体（U字溝＋ヘックス固定端）
- `bit_case_lid.stl`  — フラット蓋
- `bit_case_assembly.step` — 組立確認用

### Bambu Studio で印刷

1. 両 STL を読み込み
2. **本体**: 溝面（穴側）を上に向けて配置 → サポート不要
3. **蓋**: 内側を上に向けて配置 → サポート不要
4. PLA / レイヤー 0.2mm / Infill 20%
5. AMS Lite で本体・蓋を別色割当
6. 印刷時間目安: 本体 2.5h + 蓋 30min

## カスタマイズ

`generate.py` 冒頭のパラメータを変更:

```python
N_BITS = 15              # 本数
BIT_LENGTH = 65          # ビット長
PITCH_X = 10             # 中心間距離（密集 = 9, 余裕 = 12）
HEX_GRIP_EXTRA_DEPTH = 2 # 0 にすると uniform U字溝のみ（A型）
```

### バリエーション例

| 用途 | 変更 |
|---|---|
| **A型（uniform U字溝）** | `HEX_GRIP_EXTRA_DEPTH = 0` |
| **20本にする** | `N_BITS = 20` (外形 ~210mm、A1 miniに入らない要注意) |
| **50mm 標準ビット** | `BIT_LENGTH = 50`, `HEX_GRIP_LENGTH = 8` |
| **4mm 精密ビット** | `BIT_DIAMETER = 4.0`, `BIT_LENGTH = 28`, `PITCH_X = 6` |
| **携帯向け密集** | `PITCH_X = 9`, `BORDER_X = 3` |

## トラブルシュート

| 症状 | 対処 |
|---|---|
| ビットが溝に入らない | `CLEARANCE` を 0.2 → 0.3 |
| ビットがガバガバ | `CLEARANCE` を 0.2 → 0.1 |
| 蓋がきつい | `LID_INNER_GAP` を 0.3 → 0.4 |
| 蓋がゆるい | `LID_INNER_GAP` を 0.3 → 0.2 |
| ヘックス端固定が弱い | `HEX_GRIP_EXTRA_DEPTH` を 2 → 3 |

## 設計メモ

- **本体高 7.6mm**: 溝半径 3.6mm + 底厚 4mm。底が薄すぎると変形する
- **B型 (ヘックス端 +2mm 深溝)**: ビットを定位置にロックする効果。蓋を開けても踊らない
- **印刷向き**: 本体は溝側を上にしないとサポート必須になり、表面が荒れる
- **複数色運用**: 本体グレー / 蓋オレンジ等、視認性アップ。AMS Lite は同一PLA異色なら自動切替

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
