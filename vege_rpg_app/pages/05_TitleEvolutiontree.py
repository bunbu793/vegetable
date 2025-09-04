import streamlit as st
from modules.titles import 称号データ

st.set_page_config(page_title="称号進化ツリー", page_icon="🌳")
st.title("🌳 称号進化ツリー")

# ユーザーの称号取得状況
user_titles = st.session_state.get("titles", [])

# 進化関係を抽出
for title, data in 称号データ.items():
    if "進化先" in data:
        next_title = data["進化先"]

        with st.expander(f"🧬 {title} → {next_title}"):
            # 画像表示
            url1 = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{data['画像ファイル名']}"
            url2 = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[next_title]['画像ファイル名']}"
            st.image([url1, url2], width=120)

            # 進化条件のヒント（例：レシピ職人なら10回達成）
            if title == "レシピ初心者":
                st.markdown("📝 **進化条件**：ミッションを10回以上達成")
                # 進化達成率（例：現在の回数 / 10）
                mission_count = len(st.session_state.get("missions_completed", []))
                progress = min(mission_count / 10, 1.0)
                st.progress(progress)
                st.markdown(f"現在：{mission_count}回達成")

            elif title == "野菜コレクター":
                unique_veggies = set([m["vegetable"] for m in st.session_state.get("missions_completed", [])])
                st.markdown("📝 **進化条件**：10種類以上の野菜を救出")
                progress = min(len(unique_veggies) / 10, 1.0)
                st.progress(progress)
                st.markdown(f"現在：{len(unique_veggies)}種類")

            elif title == "図鑑研究員":
                all_vegetables = [
                    "キャベツ", "ブロッコリー", "トマト", "ニンジン", "ホウレンソウ",
                    "タマネギ", "ジャガイモ", "ピーマン", "レタス", "ダイコン",
                    "キュウリ", "ナス", "カボチャ", "サツマイモ", "アスパラガス"
                ]
                saved_veggies = set([m["vegetable"] for m in st.session_state.get("missions_completed", [])])
                complete_rate = len(saved_veggies) / len(all_vegetables)
                st.markdown("📝 **進化条件**：図鑑コンプリート率100%")
                st.progress(complete_rate)
                st.markdown(f"現在：{round(complete_rate * 100, 1)}%")

            else:
                st.markdown("📝 進化条件：この称号の進化条件はまだ設定されていません。")