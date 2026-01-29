"""
TMLE (Targeted Maximum Likelihood Estimation) 視覺化解釋
使用 Manim 製作動畫，edge-tts 中文旁白
（簡化版：不使用 LaTeX）

音頻長度參考：
- Scene01_Intro: 30.2s
- Scene02_DataTable: 31.2s
- Scene03_PS: 28.7s
- Scene04_IPTW: 35.6s
- Scene05_IPTWExample: 33.4s
- Scene06_IPTWProblem: 39.0s
- Scene07_TMLEIntro: 37.9s
- Scene08_TMLEStep1: 38.4s
- Scene09_TMLEStep2: 28.8s
- Scene10_TMLEStep3: 29.7s
- Scene11_TMLEStep4: 30.2s
- Scene12_Comparison: 46.6s
- Scene13_Summary: 42.7s
"""

import numpy as np
from manim import (
    BLUE,
    DOWN,
    DR,
    GREEN,
    LEFT,
    ORIGIN,
    PURPLE,
    RED,
    RIGHT,
    UP,
    YELLOW,
    Axes,
    Create,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    SurroundingRectangle,
    Table,
    Text,
    VGroup,
    Write,
)

# 配色方案
TREATMENT_COLOR = BLUE
CONTROL_COLOR = RED
OUTCOME_COLOR = GREEN
PS_COLOR = YELLOW
TMLE_COLOR = PURPLE


class Scene01_Intro(Scene):
    """場景1: 因果推論問題介紹 (音頻: 30.2s)"""

    def construct(self):
        title = Text("因果推論與TMLE", font_size=56, font="PingFang TC")
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP))

        question = Text(
            "核心問題：某治療對結果的因果效應是什麼？", font_size=36, font="PingFang TC"
        )
        question.next_to(title, DOWN, buff=1)
        self.play(FadeIn(question))
        self.wait(4)  # 增加等待

        challenge = VGroup(
            Text("觀察性數據的挑戰：", font_size=32, font="PingFang TC", color=YELLOW),
            Text("• 治療組和對照組不可比較", font_size=28, font="PingFang TC"),
            Text("• 存在混淆因子 (Confounders)", font_size=28, font="PingFang TC"),
            Text("• 無法直接比較結果", font_size=28, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        challenge.next_to(question, DOWN, buff=0.8)

        for item in challenge:
            self.play(FadeIn(item))
            self.wait(2)  # 每項等待更久

        # 保持畫面顯示直到音頻結束 (30.2s total)
        self.wait(8)


class Scene02_DataTable(Scene):
    """場景2: 展示觀察數據表格 (音頻: 31.2s)"""

    def construct(self):
        title = Text("觀察性數據示例", font_size=48, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        headers = ["ID", "年齡", "血壓", "治療A", "結果Y"]
        data = [
            ["1", "45", "高", "1", "好"],
            ["2", "32", "低", "0", "差"],
            ["3", "58", "高", "1", "好"],
            ["4", "41", "低", "0", "好"],
            ["5", "67", "高", "1", "差"],
            ["6", "35", "低", "1", "好"],
        ]

        table_data = [headers] + data
        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2},
        ).scale(0.6)
        table.next_to(title, DOWN, buff=0.5)

        self.play(Create(table))
        self.wait(3)  # 增加

        conf_box = SurroundingRectangle(table.get_columns()[1:3], color=YELLOW, buff=0.1)
        conf_label = Text("混淆因子 X", font_size=24, font="PingFang TC", color=YELLOW)
        conf_label.next_to(conf_box, UP)

        self.play(Create(conf_box), Write(conf_label))
        self.wait(4)  # 增加

        treat_box = SurroundingRectangle(table.get_columns()[3], color=TREATMENT_COLOR, buff=0.1)
        treat_label = Text("治療 A", font_size=24, font="PingFang TC", color=TREATMENT_COLOR)
        treat_label.next_to(treat_box, DOWN)

        out_box = SurroundingRectangle(table.get_columns()[4], color=OUTCOME_COLOR, buff=0.1)
        out_label = Text("結果 Y", font_size=24, font="PingFang TC", color=OUTCOME_COLOR)
        out_label.next_to(out_box, DOWN)

        self.play(Create(treat_box), Write(treat_label))
        self.wait(2)
        self.play(Create(out_box), Write(out_label))
        # 保持畫面顯示直到音頻結束 (31.2s total)
        self.wait(10)


class Scene03_PS(Scene):
    """場景3: 傾向分數 (Propensity Score) (音頻: 28.7s)"""

    def construct(self):
        title = Text("傾向分數 (Propensity Score)", font_size=48, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        ps_def = Text("e(X) = P(A=1 | X)", font_size=42)
        ps_def.next_to(title, DOWN, buff=0.8)

        ps_explain = Text("給定混淆因子 X，接受治療的機率", font_size=28, font="PingFang TC")
        ps_explain.next_to(ps_def, DOWN, buff=0.3)

        self.play(Write(ps_def))
        self.wait(2)
        self.play(FadeIn(ps_explain))
        self.wait(3)

        logistic = VGroup(
            Text("使用 Logistic 回歸估計：", font_size=28, font="PingFang TC"),
            Text("logit(e(X)) = β₀ + β₁X₁ + β₂X₂ + ...", font_size=32),
        ).arrange(DOWN, buff=0.3)
        logistic.next_to(ps_explain, DOWN, buff=0.8)

        self.play(FadeIn(logistic))
        self.wait(4)

        ax = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 3, 1],
            x_length=6,
            y_length=3,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.5)

        x_label = Text("傾向分數 e(X)", font_size=20, font="PingFang TC")
        x_label.next_to(ax, DOWN)

        treat_curve = ax.plot(
            lambda x: 2.5 * np.exp(-((x - 0.7) ** 2) / 0.05),
            x_range=[0.1, 1],
            color=TREATMENT_COLOR,
        )

        control_curve = ax.plot(
            lambda x: 2.5 * np.exp(-((x - 0.3) ** 2) / 0.05),
            x_range=[0, 0.9],
            color=CONTROL_COLOR,
        )

        legend = VGroup(
            VGroup(
                Line(ORIGIN, RIGHT * 0.5, color=TREATMENT_COLOR),
                Text("治療組", font_size=18, font="PingFang TC"),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Line(ORIGIN, RIGHT * 0.5, color=CONTROL_COLOR),
                Text("對照組", font_size=18, font="PingFang TC"),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(DR)

        self.play(FadeOut(VGroup(ps_def, ps_explain, logistic)))
        self.play(Create(ax), Write(x_label))
        self.play(Create(treat_curve), Create(control_curve), FadeIn(legend))
        # 保持畫面顯示直到音頻結束 (28.7s total)
        self.wait(8)


class Scene04_IPTW(Scene):
    """場景4: 逆機率加權 (IPTW) (音頻: 35.6s)"""

    def construct(self):
        title = Text("逆機率加權 IPTW", font_size=48, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        concept = Text(
            "核心思想：給每個觀察值賦予權重，創造「偽隨機化」",
            font_size=28,
            font="PingFang TC",
        )
        concept.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(concept))
        self.wait(4)  # 增加

        weight_formula = VGroup(
            Text("治療組權重：", font_size=28, font="PingFang TC"),
            Text("w₁ = 1 / e(X)", font_size=36),
        ).arrange(RIGHT, buff=0.3)

        weight_formula2 = VGroup(
            Text("對照組權重：", font_size=28, font="PingFang TC"),
            Text("w₀ = 1 / (1 - e(X))", font_size=36),
        ).arrange(RIGHT, buff=0.3)

        formulas = VGroup(weight_formula, weight_formula2).arrange(DOWN, buff=0.5)
        formulas.next_to(concept, DOWN, buff=0.8)

        self.play(FadeIn(weight_formula))
        self.wait(3)
        self.play(FadeIn(weight_formula2))
        self.wait(3)

        intuition = VGroup(
            Text("直觀理解：", font_size=28, font="PingFang TC", color=YELLOW),
            Text(
                "• PS 低但接受治療 → 權重高（稀有情況，放大）",
                font_size=24,
                font="PingFang TC",
            ),
            Text(
                "• PS 高但接受治療 → 權重低（常見情況，縮小）",
                font_size=24,
                font="PingFang TC",
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        intuition.next_to(formulas, DOWN, buff=0.8)

        for item in intuition:
            self.play(FadeIn(item))
            self.wait(3)

        # 保持畫面顯示直到音頻結束 (35.6s total)
        self.wait(8)


class Scene05_IPTWExample(Scene):
    """場景5: IPTW 計算範例表格 (音頻: 33.4s)"""

    def construct(self):
        title = Text("IPTW 計算範例", font_size=48, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        headers = ["ID", "X", "A", "e(X)", "權重 w"]
        data = [
            ["1", "高風險", "1", "0.8", "1.25"],
            ["2", "低風險", "0", "0.3", "1.43"],
            ["3", "高風險", "1", "0.7", "1.43"],
            ["4", "低風險", "1", "0.2", "5.00"],
            ["5", "高風險", "0", "0.9", "10.0"],
        ]

        table_data = [headers] + data
        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2},
        ).scale(0.55)
        table.next_to(title, DOWN, buff=0.4)

        self.play(Create(table))
        self.wait(4)  # 增加

        box1 = SurroundingRectangle(table.get_rows()[4], color=YELLOW, buff=0.05)
        box2 = SurroundingRectangle(table.get_rows()[5], color=YELLOW, buff=0.05)

        note = Text(
            "低 PS 但接受治療 或 高 PS 但未治療 → 高權重",
            font_size=24,
            font="PingFang TC",
            color=YELLOW,
        )
        note.next_to(table, DOWN, buff=0.5)

        self.play(Create(box1), Create(box2))
        self.wait(2)
        self.play(Write(note))
        self.wait(5)  # 增加

        ate = VGroup(
            Text("IPTW 估計的 ATE：", font_size=28, font="PingFang TC"),
            Text("ATE = Σwᵢ·Aᵢ·Yᵢ/Σwᵢ·Aᵢ - Σwᵢ·(1-Aᵢ)·Yᵢ/Σwᵢ·(1-Aᵢ)", font_size=24),
        ).arrange(DOWN, buff=0.3)
        ate.next_to(note, DOWN, buff=0.5)

        self.play(FadeIn(ate))
        # 保持畫面顯示直到音頻結束 (33.4s total)
        self.wait(10)


class Scene06_IPTWProblem(Scene):
    """場景6: IPTW 的問題 (音頻: 39.0s)"""

    def construct(self):
        title = Text("IPTW 的局限性", font_size=44, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # 更緊湊的排版
        p1 = VGroup(
            Text("1. 極端權重問題", font_size=28, font="PingFang TC", color=RED),
            Text("   e(X)→0或1時，權重過大，估計不穩定", font_size=22, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        p2 = VGroup(
            Text("2. 模型錯誤設定敏感", font_size=28, font="PingFang TC", color=RED),
            Text("   PS模型錯誤→估計有偏差", font_size=22, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        p3 = VGroup(
            Text("3. 效率問題", font_size=28, font="PingFang TC", color=RED),
            Text("   不是最有效率的估計方法", font_size=22, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        problems = VGroup(p1, p2, p3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        problems.next_to(title, DOWN, buff=0.5)

        for p in [p1, p2, p3]:
            self.play(FadeIn(p), run_time=0.8)
            self.wait(3)

        solution = VGroup(
            Text("解決方案：TMLE", font_size=32, font="PingFang TC", color=GREEN),
            Text("結合機器學習與半參數效率理論", font_size=24, font="PingFang TC"),
        ).arrange(DOWN, buff=0.2)
        solution.next_to(problems, DOWN, buff=0.5)

        box = SurroundingRectangle(solution, color=GREEN, buff=0.15)

        self.play(FadeIn(solution), Create(box))
        # 保持畫面顯示直到音頻結束 (39.0s total)
        self.wait(15)


class Scene07_TMLEIntro(Scene):
    """場景7: TMLE 介紹 (音頻: 37.9s)"""

    def construct(self):
        title = Text(
            "TMLE: Targeted Maximum Likelihood Estimation",
            font_size=40,
            font="PingFang TC",
        )
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        core = VGroup(
            Text("核心思想", font_size=36, font="PingFang TC", color=TMLE_COLOR),
            Text("1. 先估計結果模型 Q(A,X) = E[Y|A,X]", font_size=28, font="PingFang TC"),
            Text(
                "2. 使用 PS 構造「聰明協變量」進行目標調整",
                font_size=28,
                font="PingFang TC",
            ),
            Text(
                "3. 更新初始估計，使其針對目標參數最佳化",
                font_size=28,
                font="PingFang TC",
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        core.next_to(title, DOWN, buff=0.6)

        for item in core:
            self.play(FadeIn(item))
            self.wait(2.5)  # 每項多等

        advantages = VGroup(
            Text("TMLE 優勢：", font_size=32, font="PingFang TC", color=GREEN),
            Text(
                "✓ 雙重穩健：PS 或結果模型其一正確即可",
                font_size=26,
                font="PingFang TC",
            ),
            Text("✓ 可使用機器學習估計 nuisance 參數", font_size=26, font="PingFang TC"),
            Text("✓ 估計有效率（達到半參數效率邊界）", font_size=26, font="PingFang TC"),
            Text("✓ 提供有效的置信區間", font_size=26, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        advantages.next_to(core, DOWN, buff=0.6)

        for item in advantages:
            self.play(FadeIn(item), run_time=0.6)
            self.wait(1.5)

        # 保持畫面顯示直到音頻結束 (37.9s total)
        self.wait(8)


class Scene08_TMLEStep1(Scene):
    """場景8: TMLE 步驟 1 - 初始估計 (音頻: 38.4s)"""

    def construct(self):
        title = Text("TMLE 步驟 1：初始估計", font_size=44, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # 更緊湊的排版
        step = VGroup(
            Text("估計 Q⁰(A,X) = E[Y|A,X]", font_size=28, font="PingFang TC"),
            Text(
                "可用任何 ML 方法：GLM、RF、XGBoost、NN",
                font_size=22,
                font="PingFang TC",
            ),
            Text("推薦：Super Learner（集成方法）", font_size=22, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        step.next_to(title, DOWN, buff=0.4)

        for item in step:
            self.play(FadeIn(item))
            self.wait(3)

        pred = VGroup(
            Text("對每個觀察值計算預測：", font_size=24, font="PingFang TC", color=YELLOW),
            Text("Q̂⁰(Aᵢ, Xᵢ) = Ê[Yᵢ | Aᵢ, Xᵢ]", font_size=28),
            Text("並計算反事實預測：", font_size=24, font="PingFang TC", color=YELLOW),
            Text("Q̂⁰(1, Xᵢ) 和 Q̂⁰(0, Xᵢ)", font_size=28),
        ).arrange(DOWN, buff=0.2)
        pred.next_to(step, DOWN, buff=0.4)

        self.play(FadeIn(pred))
        # 保持畫面顯示直到音頻結束 (38.4s total)
        self.wait(15)


class Scene09_TMLEStep2(Scene):
    """場景9: TMLE 步驟 2 - 聰明協變量 (音頻: 28.8s)"""

    def construct(self):
        title = Text("TMLE 步驟 2：聰明協變量", font_size=48, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        ps_est = VGroup(
            Text("首先估計傾向分數：", font_size=28, font="PingFang TC"),
            Text("ê(X) = P̂(A=1|X)", font_size=36),
        ).arrange(DOWN, buff=0.3)
        ps_est.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(ps_est))
        self.wait(3)

        clever = VGroup(
            Text(
                "構造聰明協變量 H(A,X)：",
                font_size=32,
                font="PingFang TC",
                color=TMLE_COLOR,
            ),
            Text("H(A,X) = A/ê(X) - (1-A)/(1-ê(X))", font_size=36),
        ).arrange(DOWN, buff=0.4)
        clever.next_to(ps_est, DOWN, buff=0.6)

        self.play(FadeIn(clever))
        self.wait(3)

        explain = VGroup(
            Text("這個協變量的關鍵性質：", font_size=28, font="PingFang TC"),
            Text("• 編碼了 ATE 的影響函數方向", font_size=26, font="PingFang TC"),
            Text("• 使得調整後的估計針對 ATE 最佳化", font_size=26, font="PingFang TC"),
            Text("• 保證估計的雙重穩健性", font_size=26, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explain.next_to(clever, DOWN, buff=0.6)

        for item in explain:
            self.play(FadeIn(item), run_time=0.5)
            self.wait(1.5)

        # 保持畫面顯示直到音頻結束 (28.8s total)
        self.wait(6)


class Scene10_TMLEStep3(Scene):
    """場景10: TMLE 步驟 3 - 目標更新 (音頻: 29.7s)"""

    def construct(self):
        title = Text("TMLE 步驟 3：目標更新", font_size=48, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        update = VGroup(
            Text("用聰明協變量擬合波動參數 ε：", font_size=28, font="PingFang TC"),
            Text("logit(Q̂¹) = logit(Q̂⁰) + ε·H(A,X)", font_size=32),
        ).arrange(DOWN, buff=0.4)
        update.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(update))
        self.wait(3)

        fitting = VGroup(
            Text("擬合方式：", font_size=28, font="PingFang TC", color=YELLOW),
            Text("• 以 logit(Q⁰) 為 offset", font_size=26, font="PingFang TC"),
            Text("• 以 H(A,X) 為唯一協變量", font_size=26, font="PingFang TC"),
            Text("• 擬合 logistic 回歸得到 ε̂", font_size=26, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fitting.next_to(update, DOWN, buff=0.5)

        for item in fitting:
            self.play(FadeIn(item), run_time=0.5)
            self.wait(1.5)

        updated = VGroup(
            Text("更新後的預測：", font_size=28, font="PingFang TC", color=GREEN),
            Text("Q̂¹(A,X) = expit(logit(Q̂⁰) + ε̂·H)", font_size=32),
        ).arrange(DOWN, buff=0.3)
        updated.next_to(fitting, DOWN, buff=0.5)

        self.play(FadeIn(updated))
        # 保持畫面顯示直到音頻結束 (29.7s total)
        self.wait(10)


class Scene11_TMLEStep4(Scene):
    """場景11: TMLE 步驟 4 - 最終估計 (音頻: 30.2s)"""

    def construct(self):
        title = Text("TMLE 步驟 4：計算 ATE", font_size=48, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        counterfactual = VGroup(
            Text("使用更新後的 Q¹ 計算反事實預測：", font_size=28, font="PingFang TC"),
            Text("Q̂¹(1, Xᵢ) : 若所有人都接受治療", font_size=28),
            Text("Q̂¹(0, Xᵢ) : 若所有人都不接受治療", font_size=28),
        ).arrange(DOWN, buff=0.4)
        counterfactual.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(counterfactual))
        self.wait(4)

        ate = VGroup(
            Text("TMLE 估計的 ATE：", font_size=32, font="PingFang TC", color=TMLE_COLOR),
            Text("ATE = (1/n) Σ[Q̂¹(1,Xᵢ) - Q̂¹(0,Xᵢ)]", font_size=32),
        ).arrange(DOWN, buff=0.4)
        ate.next_to(counterfactual, DOWN, buff=0.6)

        box = SurroundingRectangle(ate, color=TMLE_COLOR, buff=0.2)

        self.play(FadeIn(ate), Create(box))
        self.wait(4)

        se = VGroup(
            Text("標準誤使用影響函數計算：", font_size=26, font="PingFang TC"),
            Text("SE = √[(1/n) Σ IC²ᵢ]", font_size=32),
        ).arrange(DOWN, buff=0.3)
        se.next_to(box, DOWN, buff=0.5)

        self.play(FadeIn(se))
        # 保持畫面顯示直到音頻結束 (30.2s total)
        self.wait(10)


class Scene12_Comparison(Scene):
    """場景12: 方法比較 (音頻: 46.6s)"""

    def construct(self):
        title = Text("方法比較", font_size=44, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        headers = ["特性", "IPTW", "TMLE"]
        data = [
            ["雙重穩健", "否", "是"],
            ["效率", "較低", "半參數有效"],
            ["ML相容", "有限", "完全支持"],
            ["極端權重", "敏感", "穩健"],
            ["置信區間", "bootstrap", "解析解"],
        ]

        table_data = [headers] + data
        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2},
            col_labels=[Text(h, font="PingFang TC", font_size=22) for h in headers],
        ).scale(0.5)
        table.next_to(title, DOWN, buff=0.4)

        self.play(Create(table))
        self.wait(20)

        conclusion = VGroup(
            Text(
                "結論：TMLE 是現代因果推論首選",
                font_size=26,
                font="PingFang TC",
                color=GREEN,
            ),
            Text("適合與機器學習結合使用", font_size=22, font="PingFang TC"),
        ).arrange(DOWN, buff=0.15)
        conclusion.next_to(table, DOWN, buff=0.35)

        box = SurroundingRectangle(conclusion, color=GREEN, buff=0.15)

        self.play(FadeIn(conclusion), Create(box))
        # 保持畫面顯示直到音頻結束 (46.6s total)
        self.wait(15)


class Scene13_Summary(Scene):
    """場景13: 總結 (音頻: 42.7s)"""

    def construct(self):
        title = Text("TMLE 總結", font_size=48, font="PingFang TC")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        steps = VGroup(
            Text("TMLE 四步驟：", font_size=30, font="PingFang TC", color=TMLE_COLOR),
            Text("1. 估計初始結果模型 Q⁰", font_size=24, font="PingFang TC"),
            Text("2. 估計 PS，構造聰明協變量 H", font_size=24, font="PingFang TC"),
            Text("3. 擬合 ε，更新得到 Q¹", font_size=24, font="PingFang TC"),
            Text("4. 用 Q¹ 計算 ATE 及 SE", font_size=24, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        steps.next_to(title, DOWN, buff=0.4)

        for item in steps:
            self.play(FadeIn(item))
            self.wait(2)

        key = VGroup(
            Text("關鍵要點：", font_size=28, font="PingFang TC", color=YELLOW),
            Text("• 雙重穩健＝兩次機會做對", font_size=22, font="PingFang TC"),
            Text("• 可放心使用機器學習", font_size=22, font="PingFang TC"),
            Text("• 半參數有效＝最佳精確度", font_size=22, font="PingFang TC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        key.next_to(steps, DOWN, buff=0.4)

        self.play(FadeIn(key))
        self.wait(8)

        thanks = Text("感謝觀看！", font_size=44, font="PingFang TC", color=GREEN)
        self.play(FadeOut(VGroup(title, steps, key)))
        self.play(Write(thanks))
        # 保持畫面顯示直到音頻結束 (42.7s total)
        self.wait(10)
