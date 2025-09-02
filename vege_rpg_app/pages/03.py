import streamlit as st
from PIL import Image
import os

image_path = "assets/images/titles/locked.png"

st.write(f"画像パス: {image_path}")
st.write(f"存在する？: {os.path.exists(image_path)}")

if os.path.exists(image_path):
    st.image("assets/images/titles/savior.png", width=150)
else:
    st.warning("画像ファイルが見つかりません")
