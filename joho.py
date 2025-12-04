import streamlit as st
import csv
import os

DATA_FILE = "data.csv"


def load_data():
    """CSV を読み込んでリストで返す"""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)


def save_data(distance, fuel, efficiency):
    """CSV に一行追加保存"""
    file_exists = os.path.exists(DATA_FILE)

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # ヘッダーがない場合のみ付ける
        if not file_exists:
            writer.writerow(["distance_km", "fuel_L", "efficiency_km_L"])

        writer.writerow([distance, fuel, efficiency])


st.set_page_config(page_title="燃費計算アプリ", layout="centered")

st.title("🚗 燃費計算")

distance = st.number_input("走行距離（km）", min_value=0.0, value=0.0, step=0.1)
fuel = st.number_input("給油量（L）", min_value=0.0, value=0.0, step=0.1)

if st.button("計算する"):
    if fuel == 0:
        st.error("給油量は 0 より大きい値を入れてください。")
    else:
        efficiency = distance / fuel
        st.success(f"燃費： {efficiency:.2f} km/L")

        save_data(distance, fuel, efficiency)

# 履歴表示
st.subheader("📜 計算履歴")

history = load_data()

if len(history) > 1:  # ヘッダー＋1行以上のとき
    st.table(history)
else:
    st.write("履歴はまだありません。")
