import streamlit as st
st.set_page_config(page_title="野菜クラフト工房", page_icon="🧪")

if "points" not in st.session_state:
    st.session_state["points"] = 0
if "money" not in st.session_state:
    st.session_state["money"] = 1000  # 初期所持金

# 所持野菜と調味料の初期化
if "owned_veggies" not in st.session_state:
    st.session_state["owned_veggies"] = ["トマト", "ナス", "チーズ"]
if "owned_seasonings" not in st.session_state:
    st.session_state["owned_seasonings"] = ["塩"]


available_veggies = [
    "トマト", "ナス", "キャベツ", "ニンジン", "ジャガイモ", "ピーマン",
    "ブロッコリー", "ホウレンソウ", "カボチャ", "サツマイモ","ダイコン",
    "キュウリ", "タマネギ", "レタス", "セロリ", "ゴボウ", "レンコン",
    "サトイモ", "カリフラワー", "アスパラガス","チーズ"
]

seasonings = ["なし", "塩", "砂糖", "醤油", "スパイス", "オリーブオイル"]

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

veggie1 = st.selectbox("材料①を選んでください", st.session_state["owned_veggies"])
veggie2 = st.selectbox("材料②を選んでください", st.session_state["owned_veggies"])
veggie3 = st.selectbox("材料③を選んでください", st.session_state["owned_veggies"])
seasoning = st.selectbox("調味料を選んでください", st.session_state["owned_seasonings"])

CRAFT_COST = 50  # 3素材クラフトはコスト高め

if st.button("クラフト開始！"):
    if st.session_state["money"] < CRAFT_COST:
        st.error("💸 マネーが足りません！クラフトできません。")
    else:
        result = craft_veggies(veggie1, veggie2, veggie3, seasoning)
        st.success(f"🎉 合成成功！{result['name']} を作成しました！")
        st.markdown(f"📝 効果：{result['effect']}")

        st.session_state["money"] -= CRAFT_COST
        st.session_state["points"] += result["points"]
        st.session_state["money"] += result["money"]

        if "craft_history" not in st.session_state:
            st.session_state["craft_history"] = []

        # 合成成功後に履歴追加
        st.session_state["craft_history"].append({
            "name": result["name"],
            "veggies": [veggie1, veggie2, veggie3],
            "seasoning": seasoning,
            "effect": result["effect"]
        })

        st.balloons()