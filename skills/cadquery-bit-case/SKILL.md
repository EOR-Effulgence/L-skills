---
name: cadquery-bit-case
description: build123d でドライバービット収納ケースを生成する。1/4 hex / 4mm 精密ビット 等のグリッド配置ケース＋スナップフィット蓋を STL/STEP 出力
category: 3d-print
---

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
