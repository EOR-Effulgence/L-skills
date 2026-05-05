"""ドライバービット収納ケース生成スクリプト（build123d）

実行:
    uv run python generate.py

出力:
    output/bit_case_base.stl
    output/bit_case_lid.stl
    output/bit_case_assembly.step
"""
from __future__ import annotations

from pathlib import Path

from build123d import (
    Align,
    Box,
    BuildPart,
    Cylinder,
    GridLocations,
    Locations,
    Mode,
    Plane,
    export_step,
    export_stl,
    Compound,
)

# ── パラメータ（ここを書き換えて再実行） ─────────────────────────
COLS = 4
ROWS = 5
BIT_LENGTH = 65          # ビット長 (mm)
HOLE_DEPTH = 55          # 穴深さ (mm) — 10mm 突き出し
HOLE_DIAMETER = 7.2      # 穴径 (mm) — 1/4 hex 7.0 + 0.2 クリアランス
PITCH = 13               # 穴中心間距離 (mm)

BORDER = 5               # 穴の縁から外壁までの距離 (mm)
WALL = 2.5               # 外壁厚 (mm)
BASE_FLOOR = 4           # 底厚 (mm)

LID_HEIGHT = 8           # 蓋の総厚 (mm)
LID_RIM_DEPTH = 5        # 蓋リップが本体に被る深さ (mm)
LID_INNER_GAP = 0.3      # 蓋と本体の隙間 (mm) — スナップフィット調整
# ─────────────────────────────────────────────────────────────


def build_base() -> BuildPart:
    inner_w = (COLS - 1) * PITCH + HOLE_DIAMETER + 2 * BORDER
    inner_l = (ROWS - 1) * PITCH + HOLE_DIAMETER + 2 * BORDER
    outer_w = inner_w + 2 * WALL
    outer_l = inner_l + 2 * WALL
    total_h = HOLE_DEPTH + BASE_FLOOR

    with BuildPart() as base:
        Box(outer_w, outer_l, total_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(Plane.XY.offset(total_h)):
            with GridLocations(PITCH, PITCH, COLS, ROWS):
                Cylinder(
                    radius=HOLE_DIAMETER / 2,
                    height=HOLE_DEPTH,
                    align=(Align.CENTER, Align.CENTER, Align.MAX),
                    mode=Mode.SUBTRACT,
                )
    return base


def build_lid() -> BuildPart:
    inner_w = (COLS - 1) * PITCH + HOLE_DIAMETER + 2 * BORDER
    inner_l = (ROWS - 1) * PITCH + HOLE_DIAMETER + 2 * BORDER
    outer_w = inner_w + 2 * WALL
    outer_l = inner_l + 2 * WALL

    rim_inner_w = inner_w + LID_INNER_GAP
    rim_inner_l = inner_l + LID_INNER_GAP

    with BuildPart() as lid:
        Box(outer_w, outer_l, LID_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Box(
            rim_inner_w,
            rim_inner_l,
            LID_RIM_DEPTH,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )
    return lid


def main() -> None:
    out = Path(__file__).parent / "output"
    out.mkdir(exist_ok=True)

    base = build_base()
    lid = build_lid()

    export_stl(base.part, str(out / "bit_case_base.stl"))
    export_stl(lid.part, str(out / "bit_case_lid.stl"))

    total_h = HOLE_DEPTH + BASE_FLOOR
    lid_positioned = lid.part.moved(
        Plane.XY.offset(total_h + 2).location
    )
    assembly = Compound(label="bit_case", children=[base.part, lid_positioned])
    export_step(assembly, str(out / "bit_case_assembly.step"))

    inner_w = (COLS - 1) * PITCH + HOLE_DIAMETER + 2 * BORDER
    inner_l = (ROWS - 1) * PITCH + HOLE_DIAMETER + 2 * BORDER
    outer_w = inner_w + 2 * WALL
    outer_l = inner_l + 2 * WALL

    print(
        f"\n生成完了:\n"
        f"  穴: {COLS}列×{ROWS}行 = {COLS * ROWS}本\n"
        f"  外形: {outer_w:.1f} × {outer_l:.1f} × {total_h:.1f}mm (本体)\n"
        f"  蓋:   {outer_w:.1f} × {outer_l:.1f} × {LID_HEIGHT:.1f}mm\n"
        f"  → {out}/"
    )


if __name__ == "__main__":
    main()
