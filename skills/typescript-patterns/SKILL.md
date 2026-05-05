---
name: typescript-patterns
description: TypeScript プロジェクトのベストプラクティスとパターン集（mise / strict tsconfig / zod / monorepo）
category: development
---

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
