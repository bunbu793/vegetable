import streamlit as st

# 称号一覧と説明
称号データ = {
    "冷蔵庫の救世主": {
        "説明": "ミッションを3回達成した者に与えられる称号。",
        "レア度":"★☆☆☆☆",
        "画像ファイル名": "savior.png"
    },
    "アンデッドキラー": {
        "説明": "ゾンビ度80%以上の野菜を5回以上救出した者に与えられる称号。",
        "画像ファイル名": "undead_killer.png",
        "レア度": "★★★"
    },
    "フレッシュ守護神": {
        "説明": "ゾンビ度30%未満の野菜を3回救出した者に与えられる称号。",
        "画像ファイル名": "fresh_guardian.png",
        "レア度": "★★☆",
    },
    "レシピ初心者": {
        "説明": "ミッションを1回達成した者に与えられる称号。",
        "画像ファイル名": "recipe_beginner.png",
        "レア度": "★☆☆",
        "進化先": "レシピ職人"
    },
    "レシピ職人": {
        "説明": "ミッションを10回以上達成した者に与えられる称号。",
        "画像ファイル名": "recipe_master.png",
        "レア度": "★★★"
    },
    "野菜コレクター": {
        "説明": "5種類以上の野菜を救出した者に与えられる称号。",
        "画像ファイル名": "vege_collector.png",
        "レア度": "★★☆",
        "進化先": "ベジマスター"
    },
    "ベジマスター": {
        "説明": "10種類以上の野菜を救出した者に与えられる称号。",
        "画像ファイル名": "vege_master.png",
        "レア度": "★★★"
    },
    "図鑑研究員": {
        "説明": "図鑑コンプリート率が50%以上の者に与えられる称号。",
        "画像ファイル名": "dictionary_researcher.png",
        "レア度": "★★☆",
        "進化先": "図鑑マスター"
    },
    "図鑑マスター": {
        "説明": "すべての野菜を救出し、図鑑をコンプリートした者に与えられる称号。",
        "画像ファイル名": "dictionary_master.png",
        "レア度": "★★★★★"
    },
    "ミッションマニア": {
        "説明": "ミッションを20回以上達成した者に与えられる称号。",
        "画像ファイル名": "mission_maniac.png",
        "レア度": "★★★"
    },
    "トマトの守護者": {
        "説明": "トマトを5回以上救出した者に与えられる称号。",
        "画像ファイル名": "tomato_guardian.png",
        "レア度": "★★☆"
    },
    "根菜の王": {
        "説明": "ニンジン・ダイコン・ジャガイモを各3回以上救出した者に与えられる称号。",
        "画像ファイル名": "root_king.png",
        "レア度": "★★★"
    },
    "葉っぱマスター": {
        "説明": "レタス・ホウレンソウ・キャベツを各3回以上救出した者に与えられる称号。",
        "画像ファイル名": "leaf_master.png",
        "レア度": "★★★"
    },
    "腐っても野菜": {
        "説明": "ゾンビ度100%の野菜を診断した者に与えられる称号。",
        "画像ファイル名": "still_vegetable.png",
        "レア度": "★☆☆"
    },
    "野菜の友達": {
        "説明": "同じ野菜を10回以上救出した者に与えられる称号。",
        "画像ファイル名": "vege_friend.png",
        "レア度": "★★★"
    }

}



def get_title_info(title_name):
    return 称号データ.get(title_name, "説明なし")

def check_titles(mission_history, existing_titles=None):
    if existing_titles is None:
        existing_titles = []

    new_titles = []

    # 称号条件①：ミッション3回達成
    if len(mission_history) >= 3 and "冷蔵庫の救世主" not in existing_titles:
        new_titles.append("冷蔵庫の救世主")

        # ゾンビ度系
    high_zombie = [m for m in mission_history if m["zombie_score"] >= 80]
    low_zombie = [m for m in mission_history if m["zombie_score"] < 30]
    full_zombie = [m for m in mission_history if m["zombie_score"] == 100]

    if len(high_zombie) >= 5 and "アンデッドキラー" not in existing_titles:
        new_titles.append("アンデッドキラー")

    if len(low_zombie) >= 3 and "フレッシュ守護神" not in existing_titles:
        new_titles.append("フレッシュ守護神")
    if len(low_zombie) >= 10 and "冷蔵庫の精霊" not in existing_titles:
        new_titles.append("冷蔵庫の精霊")

    if full_zombie and "腐っても野菜" not in existing_titles:
        new_titles.append("腐っても野菜")

    # ミッション回数系
    if len(mission_history) >= 1 and "レシピ初心者" not in existing_titles:
        new_titles.append("レシピ初心者")
    if len(mission_history) >= 10 and "レシピ職人" not in existing_titles:
        new_titles.append("レシピ職人")
    if len(mission_history) >= 20 and "ミッションマニア" not in existing_titles:
        new_titles.append("ミッションマニア")

    # 野菜種類系
    unique_veggies = set([m["vegetable"] for m in mission_history])
    if len(unique_veggies) >= 5 and "野菜コレクター" not in existing_titles:
        new_titles.append("野菜コレクター")
    if len(unique_veggies) >= 10 and "ベジマスター" not in existing_titles:
        new_titles.append("ベジマスター")

    # 図鑑コンプリート率系
    all_vegetables = [
        "キャベツ", "ブロッコリー", "トマト", "ニンジン", "ホウレンソウ",
        "タマネギ", "ジャガイモ", "ピーマン", "レタス", "ダイコン",
        "キュウリ", "ナス", "カボチャ", "サツマイモ", "アスパラガス"
    ]
    saved_veggies = set([m["vegetable"] for m in mission_history])
    complete_rate = len(saved_veggies) / len(all_vegetables)

    if complete_rate >= 0.5 and "図鑑研究員" not in existing_titles:
        new_titles.append("図鑑研究員")
    if complete_rate == 1.0 and "図鑑マスター" not in existing_titles:
        new_titles.append("図鑑マスター")

    # 野菜別称号
    tomato_count = len([m for m in mission_history if m["vegetable"] == "トマト"])
    if tomato_count >= 5 and "トマトの守護者" not in existing_titles:
        new_titles.append("トマトの守護者")

    root_veggies = ["ニンジン", "ダイコン", "ジャガイモ"]
    if all([len([m for m in mission_history if m["vegetable"] == v]) >= 3 for v in root_veggies]) and "根菜の王" not in existing_titles:
        new_titles.append("根菜の王")

    leaf_veggies = ["レタス", "ホウレンソウ", "キャベツ"]
    if all([len([m for m in mission_history if m["vegetable"] == v]) >= 3 for v in leaf_veggies]) and "葉っぱマスター" not in existing_titles:
        new_titles.append("葉っぱマスター")

    # 同じ野菜を10回以上救出
    for veg in unique_veggies:
        count = len([m for m in mission_history if m["vegetable"] == veg])
        if count >= 10 and "野菜の友達" not in existing_titles:
            new_titles.append("野菜の友達")
            break  # 一度獲得すればOK

    return new_titles
