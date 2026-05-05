"""ドライバービット横置き収納ケース（薄型タックルボックス型）

15本を平らに並べる薄型ケース。U字溝に横向きでセット、フラット蓋でスナップ閉じ。
B型 = ヘックス固定端（深溝）+ 軸受溝（U字チャネル）

実行:
    uv run python generate.py
"""
from __future__ import annotations

from pathlib import Path

from build123d import (
    Align,
    Box,
    BuildPart,
    Compound,
    Cylinder,
    Locations,
    Mode,
    export_step,
    export_stl,
)

# ── パラメータ（書き換えて再実行） ─────────────────────────
N_BITS = 15              # 本数
BIT_LENGTH = 65          # ビット長 (mm)
BIT_DIAMETER = 7.0       # ビット六角対角 (mm)
CLEARANCE = 0.2          # 嵌合クリアランス (mm)

PITCH_X = 10             # 中心間距離 (mm)
BORDER_X = 5             # 左右余白
BORDER_Y = 5             # 前後余白
WALL = 2.5               # 外壁厚
BASE_FLOOR = 4           # 底厚

# B型: ヘックス固定端
HEX_GRIP_LENGTH = 10     # 端の深溝長さ (mm)
HEX_GRIP_EXTRA_DEPTH = 2 # 通常溝より追加で掘る深さ (mm)

LID_HEIGHT = 6           # 蓋総厚
LID_RIM_DEPTH = 4        # 蓋リップ被り
LID_INNER_GAP = 0.3      # 蓋スナップクリアランス
# ───────────────────────────────────────────────────────


def calc_dims() -> tuple[float, float, float, float, float]:
    channel_d = BIT_DIAMETER + CLEARANCE
    inner_w = (N_BITS - 1) * PITCH_X + channel_d + 2 * BORDER_X
    inner_l = BIT_LENGTH + 2 * BORDER_Y
    outer_w = inner_w + 2 * WALL
    outer_l = inner_l + 2 * WALL
    body_h = channel_d / 2 + BASE_FLOOR
    return inner_w, inner_l, outer_w, outer_l, body_h


def build_base() -> BuildPart:
    channel_d = BIT_DIAMETER + CLEARANCE
    radius = channel_d / 2
    iw, il, ow, ol, h = calc_dims()
    channel_len = BIT_LENGTH + 2  # ビットより2mm長い溝

    with BuildPart() as base:
        Box(ow, ol, h, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 主溝: U字チャネル（軸を支える）
        for i in range(N_BITS):
            x = (i - (N_BITS - 1) / 2) * PITCH_X
            with Locations((x, 0, h)):
                Cylinder(
                    radius=radius,
                    height=channel_len,
                    rotation=(90, 0, 0),
                    mode=Mode.SUBTRACT,
                )

        # 副溝: ヘックス固定端（片側に深く掘る）
        if HEX_GRIP_EXTRA_DEPTH > 0:
            grip_y_center = -BIT_LENGTH / 2 + HEX_GRIP_LENGTH / 2 + 2
            for i in range(N_BITS):
                x = (i - (N_BITS - 1) / 2) * PITCH_X
                with Locations((x, grip_y_center, h - HEX_GRIP_EXTRA_DEPTH)):
                    Cylinder(
                        radius=radius,
                        height=HEX_GRIP_LENGTH,
                        rotation=(90, 0, 0),
                        mode=Mode.SUBTRACT,
                    )
    return base


def build_lid() -> BuildPart:
    iw, il, ow, ol, _h = calc_dims()
    rim_iw = iw + LID_INNER_GAP
    rim_il = il + LID_INNER_GAP
    with BuildPart() as lid:
        Box(ow, ol, LID_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Box(
            rim_iw,
            rim_il,
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
    iw, il, ow, ol, h = calc_dims()

    export_stl(base.part, str(out / "bit_case_base.stl"))
    export_stl(lid.part, str(out / "bit_case_lid.stl"))

    from build123d import Plane

    lid_positioned = lid.part.moved(Plane.XY.offset(h + 1).location)
    assembly = Compound(label="bit_case", children=[base.part, lid_positioned])
    export_step(assembly, str(out / "bit_case_assembly.step"))

    print(
        f"\n生成完了（横置き B型）:\n"
        f"  本数: {N_BITS}本（1段、横置き）\n"
        f"  外形: {ow:.1f} × {ol:.1f} × {h:.1f}mm（本体）\n"
        f"        蓋 {ow:.1f} × {ol:.1f} × {LID_HEIGHT:.1f}mm\n"
        f"  合計厚: {h + LID_HEIGHT - LID_RIM_DEPTH:.1f}mm\n"
        f"  ヘックス固定端: 深さ +{HEX_GRIP_EXTRA_DEPTH}mm × {HEX_GRIP_LENGTH}mm\n"
        f"  → {out}/"
    )


if __name__ == "__main__":
    main()
