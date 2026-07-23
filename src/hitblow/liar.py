# src/hitblow/liar.py
import random


def make_lie(real_hit, real_blow, digits=3):
    """実際の判定 (hit, blow) から、ルール上破綻しない嘘の判定を生成する。"""
    # すでに3ヒット（完全正解）している場合は嘘をつけない（ゲームが終わらなくなるため）
    if real_hit == digits:
        return real_hit, real_blow

    possible_lies = []

    # パターンA: Hit数を1減らす (元が0より大きい場合)
    if real_hit > 0:
        possible_lies.append((real_hit - 1, real_blow))
    # パターンB: Blow数を1減らす (元が0より大きい場合)
    if real_blow > 0:
        possible_lies.append((real_hit, real_blow - 1))
    # パターンC: 合計数が桁数を超えない範囲で、Hit数を1増やす
    if real_hit + real_blow < digits:
        possible_lies.append((real_hit + 1, real_blow))

    # 万が一、嘘の選択肢が作れなかった場合はそのまま本物を返す
    if not possible_lies:
        return real_hit, real_blow

    # 嘘候補からランダムに1つ選んで返す
    return random.choice(possible_lies)