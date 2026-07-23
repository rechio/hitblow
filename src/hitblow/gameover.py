# gameover.py

def check_game_over(tries):
    if tries >= 7:
        print("挑戦回数が7回に達しました。ゲームオーバーです。")
        return True
    return False
