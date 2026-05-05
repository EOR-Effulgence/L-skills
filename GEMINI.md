# GEMINI.md

L-skills の知見集（Codex / GitHub Copilot CLI 用、自動生成）

## 一覧

- **python-patterns**: Python プロジェクトのベストプラクティスとパターン集（uv / pydantic / pytest / イミュータブル）
- **rust-patterns**: Rust プロジェクトのベストプラクティスとパターン集（cargo workspace / clippy / thiserror / anyhow）
- **typescript-patterns**: TypeScript プロジェクトのベストプラクティスとパターン集（mise / strict tsconfig / zod / monorepo）

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
