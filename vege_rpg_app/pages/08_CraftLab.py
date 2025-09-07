from streamlit_extras.let_it_rain import rain
import requests
import streamlit as st
st.set_page_config(page_title="野菜クラフト工房", page_icon="🧪")

if "points" not in st.session_state:
    st.session_state["points"] = 0
if "money" not in st.session_state:
    st.session_state["money"] = 1000  # 初期所持金

# 所持野菜と調味料の初期化
if "owned_veggies" not in st.session_state:
    st.session_state["owned_veggies"] = {
        "トマト": 1,
        "ナス": 1,
        "チーズ": 1
    }
if "owned_seasonings" not in st.session_state:
    st.session_state["owned_seasonings"] = {
        "塩": 1
    }

available_veggies = [
    "トマト", "ナス", "キャベツ", "ニンジン", "ジャガイモ", "ピーマン",
    "ブロッコリー", "ホウレンソウ", "カボチャ", "サツマイモ","ダイコン",
    "キュウリ", "タマネギ", "レタス", "セロリ", "ゴボウ", "レンコン",
    "サトイモ", "カリフラワー", "アスパラガス","チーズ"
]

seasonings = ["なし", "塩", "砂糖", "醤油", "スパイス", "オリーブオイル"]

def consume_veggies(v1, v2, v3):
    used = []
    for v in [v1, v2, v3]:
        if st.session_state["owned_veggies"].get(v, 0) > 0:
            st.session_state["owned_veggies"][v] -= 1
            used.append(v)
        else:
            st.error(f"❌ {v} の在庫が足りません！")
            return False
    st.info("🧺 使用した素材：" + "、".join([f"{v}（残りx{st.session_state['owned_veggies'][v]}）" for v in used]))
    return True

def consume_seasoning(s):
    if st.session_state["owned_seasonings"].get(s, 0) > 0:
        st.session_state["owned_seasonings"][s] -= 1
        st.info(f"🧂 使用した調味料：{s}（残りx{st.session_state['owned_seasonings'][s]}）")
        return True
    else:
        st.error(f"❌ 調味料「{s}」の在庫が足りません！")
        return False

def craft_veggies(v1, v2, v3, seasoning):
    recipes = {
        tuple(sorted(["トマト", "ナス", "チーズ"])): {
            "name": "トマナスチーズグラタン",
            "effect": "ポイント+20 / マネー+80",
            "points": 20,
            "money": 80
        },
        tuple(sorted(["キャベツ", "ニンジン", "ジャガイモ"])): {
            "name": "彩り野菜ポトフ",
            "effect": "ポイント+15 / マネー+60",
            "points": 15,
            "money": 60
        }
    }
    key = tuple(sorted([v1, v2, v3]))
    result = recipes.get(key, {
        "name": "失敗作",
        "effect": "何も起こらない…",
        "points": 0,
        "money": 0
    })

    # 調味料の効果を追加
    if seasoning == "塩":
        result["points"] += 2
    elif seasoning == "砂糖":
        result["money"] += 10
    elif seasoning == "醤油":
        result["points"] += 5
    elif seasoning == "スパイス" and result["name"] == "失敗作":
        result["name"] = "スパイスミラクル"
        result["effect"] = "レアレシピ発動！ポイント+30 / マネー+100"
        result["points"] = 30
        result["money"] = 100
    elif seasoning == "オリーブオイル":
        result["effect"] += " / ゾンビ度-10%"

    return result

st.subheader("🧪 野菜クラフト工房")
st.metric("所持ポイント", f"{st.session_state['points']} pt")
st.metric("所持マネー", f"🪙{st.session_state['money']}マネー")
def get_available_veggies():
    return [f"{v}（x{count}）" for v, count in st.session_state["owned_veggies"].items() if count > 0]

def extract_name(label):
    if isinstance(label, str):
        return label.split("（")[0]

veggie_options = get_available_veggies()
if veggie_options:
    veggie1_label = st.selectbox("材料①を選んでください", veggie_options)
    veggie2_label = st.selectbox("材料②を選んでください", veggie_options)
    veggie3_label = st.selectbox("材料③を選んでください", veggie_options)

    veggie1 = extract_name(veggie1_label)
    veggie2 = extract_name(veggie2_label)
    veggie3 = extract_name(veggie3_label)
else:
    st.warning("🥕 材料が足りないよ！まずは野菜をゲットしてね！")

def get_available_seasonings():
    return [f"{s}（x{count}）" for s, count in st.session_state["owned_seasonings"].items() if count > 0]

seasoning_label = st.selectbox("調味料を選んでください", get_available_seasonings())
seasoning = extract_name(seasoning_label)

CRAFT_COST = 50  # 3素材クラフトはコスト高め
if st.button("クラフト開始！"):
    if st.session_state["money"] < CRAFT_COST:
        st.error("💸 マネーが足りません！クラフトできません。")
    else:
        result = craft_veggies(veggie1, veggie2, veggie3, seasoning)

        if result["name"] != "失敗作":
            if consume_veggies(veggie1, veggie2, veggie3) and consume_seasoning(seasoning):
                st.success(f"🎉 合成成功！{result['name']} を作成したぜ！")
                st.markdown(f"📝 効果：{result['effect']}")

                st.session_state["money"] -= CRAFT_COST
                st.session_state["points"] += result["points"]
                st.session_state["money"] += result["money"]

                if "craft_history" not in st.session_state:
                    st.session_state["craft_history"] = []

                st.session_state["craft_history"].append({
                    "name": result["name"],
                    "veggies": [veggie1, veggie2, veggie3],
                    "seasoning": seasoning,
                    "effect": result["effect"]
                })

                rain(
                    emoji = "✨",

                    font_size = 54,

                    falling_speed = 5,
                    
                    animation_length = "short"
                )
        else:
            st.warning("😢 合成失敗…素材はそのまま残ってるよ。次こそリベンジだ！")
