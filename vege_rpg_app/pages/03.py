import streamlit as st
from PIL import Image
import os

image_path = "assets/images/titles/locked.png"

st.write(f"画像パス: {image_path}")
st.write(f"存在する？: {os.path.exists(image_path)}")

if os.path.exists(image_path):
    try:
        img = Image.open(image_path)
        st.image(img, caption="未開放称号", width=150)
    except Exception as e:
        st.error(f"画像の読み込みに失敗しました：{e}")
else:
    st.warning("画像ファイルが見つかりません")
