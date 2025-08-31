import random

# 仮のレシピデータベース
RECIPE_DB = {
    "トマト": ["トマトパスタ", "カプレーゼ", "トマトスープ"],
    "ナス": ["麻婆ナス", "ナスの揚げびたし", "ナスグラタン"],
    "キャベツ": ["キャベツ炒め", "コールスロー", "ロールキャベツ"],
    "ピーマン": ["ピーマンの肉詰め", "青椒肉絲", "ピーマン炒め"]
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
    mission_text = f"{urgency} この{vegetable_name}を使って『{recipe}』を作れ！ゾンビ化度：{zombie_score}%"

    return {
        "vegetable": vegetable_name,
        "zombie_score": zombie_score,
        "recipe": recipe,
        "urgency": urgency,
        "mission": mission_text
    }