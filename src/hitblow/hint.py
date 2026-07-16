# hitblow/hint.py


def get_sum_hint(secret):
    """正解の文字列（例: "123"）の各桁の合計値を計算して返す。"""
    # 各文字を数値に変換して合計する
    total_sum = sum(int(digit) for digit in secret)
    return total_sum