---
name: rust-patterns
description: Rust プロジェクトのベストプラクティスとパターン集（cargo workspace / clippy / thiserror / anyhow）
category: development
---

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
