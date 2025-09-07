import streamlit as st
from modules.mission import RECIPE_DB  # 野菜一覧を使うなら

st.set_page_config(page_title="クラフト工房", page_icon="🧪")
st.title("🧪 野菜クラフト工房")

# 仮の野菜一覧（RECIPE_DBのキーを使う）
available_veggies = list(RECIPE_DB.keys())

veggie1 = st.selectbox("材料①を選んでください", available_veggies)
veggie2 = st.selectbox("材料②を選んでください", available_veggies)

def craft_veggies(v1, v2):
    recipes = {
        ("トマト", "ナス"): {"name": "トマナスグラタン", "effect": "ポイント+10"},
        ("キャベツ", "ニンジン"): {"name": "彩りサラダ", "effect": "ゾンビ度-15%"},
        ("サツマイモ", "カボチャ"): {"name": "甘味ブースター", "effect": "経験値2倍"},
    }
    key = tuple(sorted([v1, v2]))
    return recipes.get(key, {"name": "失敗作", "effect": "何も起こらない…"})

if st.button("クラフト開始！"):
    result = craft_veggies(veggie1, veggie2)
    st.success(f"🎉 合成成功！{result['name']} を作成しました！")
    st.markdown(f"📝 効果：{result['effect']}")
    st.balloons()