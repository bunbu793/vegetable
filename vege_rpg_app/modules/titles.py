import streamlit as st

# 称号一覧と説明
称号データ = {
    "冷蔵庫の救世主": {
        "説明": "ミッションを3回達成した者に与えられる称号。",
        "画像ファイル名": "savior.png"
    },
    "アンデッドキラー": {
        "説明": "ゾンビ度80%以上の野菜を2回救った者に与えられる称号。",
        "画像ファイル名": "undead_killer.png"
    },
    "ベジマスター": {
        "説明": "4種類以上の野菜を使った者に与えられる称号。",
        "画像ファイル名": "vege_master.png"
    },
    "野菜語り部": {
        "説明": "5種類以上の野菜を使った者に与えられる称号。",
        "画像ファイル名": "vege_master.png"
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

    # 称号条件②：ゾンビ度80%以上のミッションを2回達成
    high_zombie_missions = [m for m in mission_history if m["zombie_score"] >= 80]
    if len(high_zombie_missions) >= 2 and "アンデッドキラー" not in existing_titles:
        new_titles.append("アンデッドキラー")

    # 称号条件③：4種類以上の野菜を使った
    unique_veggies = set([m["vegetable"] for m in mission_history])
    if len(unique_veggies) >= 4 and "ベジマスター" not in existing_titles:
        new_titles.append("ベジマスター")

    # 称号条件④：5種類以上の野菜を使った
    if len(unique_veggies) >= 5 and "野菜語り部" not in existing_titles:
        new_titles.append("野菜語り部")

    if st.session_state.get("viewed_rules") and "ルールマスター" not in existing_titles:
        new_titles.append("ルールマスター")

    return new_titles
