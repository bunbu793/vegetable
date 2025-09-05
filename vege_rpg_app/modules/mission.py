import random

REWARD_POINTS = {
    "トマト": 5,
    "ジャガイモ": 3,
    "ニンジン": 4,
    "キャベツ": 2,
    "ナス": 3,
    "ピーマン": 2,
    "ブロッコリー": 4,
    "ホウレンソウ": 3,
    "タマネギ": 2,
    "レタス": 2,
    "ダイコン": 3,
    "キュウリ": 2,
    "カボチャ": 4,
    "サツマイモ": 5,
    "アスパラガス": 3
}

# 仮のレシピデータベース
RECIPE_DB = {
    "トマト": ["トマトパスタ", "カプレーゼ", "トマトスープ"],
    "ナス": ["麻婆ナス", "ナスの揚げびたし", "ナスグラタン"],
    "キャベツ": ["キャベツ炒め", "コールスロー", "ロールキャベツ"],
    "ピーマン": ["ピーマンの肉詰め", "青椒肉絲", "ピーマン炒め"],
    "ブロッコリー": ["ブロッコリーの炒め物", "ブロッコリーのサラダ", "ブロッコリーのクリーム煮"],
    "ニンジン": ["ニンジンのグラッセ", "ニンジンのきんぴら", "ニンジンのポタージュ"],
    "ホウレンソウ": ["ホウレンソウのおひたし", "ホウレンソウのソテー", "ホウレンソウのクリームパスタ"],
    "タマネギ": ["タマネギのスープ", "タマネギのマリネ", "タマネギのオーブン焼き"],
    "ジャガイモ": ["ジャガイモの煮っ転がし", "ジャガイモのグラタン", "ジャガイモのサラダ"],
    "レタス": ["レタスのサラダ", "レタスの巻き寿司", "レタスのスープ"],
    "ダイコン": ["ダイコンの漬物", "ダイコンの煮物", "ダイコンのサラダ"],
    "キュウリ": ["キュウリの酢の物", "キュウリのサラダ", "キュウリの漬物"],
    "カボチャ": ["カボチャの煮物", "カボチャのサラダ", "カボチャのスープ"],
    "サツマイモ": ["サツマイモの焼き芋", "サツマイモのサラダ", "サツマイモのスイートポテト"],
    "アスパラガス": ["アスパラガスの炒め物", "アスパラガスのサラダ", "アスパラガスのグリル"]
}

HIDDEN_VEGETABLES = {
    "アボカド": {
        "解放条件": "レアレシピ解放券",
        "レシピ": ["アボカドサラダ", "アボカドディップ"]
    },
    "ケール": {
        "解放条件": "レアレシピ解放券",
        "レシピ": ["ケールスムージー", "ケール炒め"]
    }
}
# ミッション生成関数
def generate_mission(vegetable_name, zombie_score):
    urgency = ""
    if zombie_score >= 80:
        urgency = "🔥緊急ミッション！"
    elif zombie_score >= 60:
        urgency = "⚠️ 早めに対応せよ！"
    else:
        urgency = "🧘‍♂️ のんびりミッション"

    recipe = random.choice(RECIPE_DB.get(vegetable_name, ["未知のレシピ"]))

    reward_points = REWARD_POINTS.get(vegetable_name, 1)
    mission_text = f"{urgency} この{vegetable_name}を使って『{recipe}』を作れ！ゾンビ化度：{zombie_score}%"

    # レシピ選択（通常 or 隠し）
    if vegetable_name in HIDDEN_VEGETABLES:
        recipe = random.choice(HIDDEN_VEGETABLES[vegetable_name]["レシピ"])
    else:
        recipe = random.choice(RECIPE_DB.get(vegetable_name, ["未知のレシピ"]))

    return {
        "vegetable": vegetable_name,
        "zombie_score": zombie_score,
        "recipe": recipe,
        "urgency": urgency,
        "mission": mission_text,
        "reward_points": reward_points
    }
__all__ = ["generate_mission", "RECIPE_DB", "HIDDEN_VEGETABLES"]