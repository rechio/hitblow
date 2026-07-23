"""ゲームの進行（入力・表示・ループ）。

★ チームで足す機能は **自分の担当の場所**に書く（1機能=1ファイル）。
    下の「ここに足す」場所は3か所（① 開始時 ② 入力コマンド ③ 勝利時）。
    ペアごとに**別の場所**を直すので、並行作業でも衝突しない。
    import も自分の場所の近くに書くこと（ファイル先頭にまとめない＝衝突回避）。
"""

from .core import judge, make_secret


def play(digits=3):
    secret = make_secret(digits)
    print(f"Hit & Blow（{digits} 桁・重複なし）")

    # ===== ① 開始時に足す（難易度・あいさつ など）: ここに書く =====
    # 嘘つきモード用の変数を初期化
    has_lied = False  # 実際に嘘をついたかどうかのフラグ
    lie_turn = 0  # 嘘をついたターン（tries）
    doubt_used = False  # プレイヤーがダウト権を使ったか
    last_real = (0, 0)  # 直前の「本当の」判定を記録
    last_displayed = (0, 0)  # 直前の「表示した」判定を記録

    # 3〜7回目の間で、ランダムに1回だけ嘘をつくタイミングを決める
    import random

    lie_trigger_turn = random.randint(3, 7)
    print("😈 [ブラフモード] コンピューターはゲーム中、1回だけ嘘の判定を返します。")
    print("   違和感を感じたら、次の手番で 'doubt' と入力してください！")
    # ===============================================================

    tries = 0
    while True:
        guess = input("予想 > ").strip()

        # ===== ② 入力コマンドに足す（ヒント など）: ここに書く（import もここに） =====
        # --- ダウト判定コマンド ---
        if guess == "doubt":
            if doubt_used:
                print("❌ ダウト権は1ゲームに1回しか使えません！")
                continue
            if tries == 0:
                print("❌ まだ誰も予想していません！")
                continue

            doubt_used = True

            # 直前の表示と実際の判定が食い違っていればダウト成功
            if last_displayed != last_real:
                print("🎉 【ダウト成功！】コンピューターの嘘を見破った！")
                print("🎁 報酬として、すべての正解を公開します！")
                print(
                    f"👑 お見事！大勝利です！（答え：{secret} / かかった手数：{tries} 回）"
                )
                break  # その場で即時ゲーム終了
            else:
                print("💀 【ダウト失敗！】直前の判定は本当でした。")
                print("⚠️ ペナルティとして、挑戦回数が +3 されます！")
                tries += 3
            continue
        # ==============================================================================

        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してね")
            continue
        tries += 1
        # --- ゲームオーバー判定（挑戦回数7回） ---
        from .gameover import check_game_over
        if check_game_over(tries):
            break

        if tries == 5:
            # 5回目の入力時に、自作したhintモジュールから関数をインポートして実行
            from .hint import get_sum_hint

            secret_sum = get_sum_hint(secret)
            print(
                f"💡 [5回目ヒント] 答えの3つの数字をすべて足すと 【 {secret_sum} 】 です！"
            )

        hit, blow = judge(secret, guess)

        # 判定を記録しておく
        last_real = (hit, blow)

        # --- 嘘をつくタイミングの判定（3〜7ターンの間でランダム、かつ正解（3ヒット）ではない場合） ---
        if tries == lie_trigger_turn and not has_lied and hit != digits:
            from .liar import make_lie

            # 嘘の判定を生成して上書きする
            hit, blow = make_lie(hit, blow, digits)
            has_lied = True
            lie_turn = tries

        # 画面に実際に表示した判定を記録
        last_displayed = (hit, blow)

        print(f"  Hit={hit}  Blow={blow}")

        # ※嘘判定（hit=3）で上がってしまうのを防ぐため、本物の判定（last_real[0]）でクリア判定する
        if last_real[0] == digits:

            # ===== ③ 勝利時に足す（スコア・履歴 など）: ここに書く =====
            if has_lied:
                print(
                    f"🤫 実は第 {lie_turn} 手目で嘘の判定を出していました！"
                )
            else:
                print("😇 今回は嘘をつく前に正解されてしまいました！")
            # ===========================================================

            print(f"正解！ {tries} 回で当たり（答え {secret}）")
            break