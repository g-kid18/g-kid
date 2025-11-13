
# app.py
# 必要: pip install streamlit
from typing import List, Dict
import streamlit as st
import html
import unicodedata
import json

# -----------------------
# サンプル曲データ（ここを実データに書き換える）
# -----------------------
SONGS: List[Dict] = [
    {"id": 1, "title": "oneway Drive", "album": "Midnight Drive", "year": 2020,
     "lyrics": "夜空の下で 君と", "tags": ["pop", "2020"],
     "url": "https://www.youtube.com/results?search_query=g-kid+starry+night"},
    {"id": 2, "title": "Summer Echo", "album": "Sunset Tape", "year": 2019,
     "lyrics": "風が運ぶメロディ", "tags": ["indie", "2019"],
     "url": "https://www.youtube.com/results?search_query=g-kid+summer+echo"},
    {"id": 3, : "Hikari", "album": "Neon Road", "year": 2021,
     "lyrics": "光が刺す方へ", "tags": ["electronic", "2021"],
     "url": "https://www.youtube.com/results?search_query=g-kid+hikari"},
    # 必要ならここに追加
]

# -----------------------
# ユーティリティ
# -----------------------
def normalize(text: str) -> str:
    """小文字化 + 全角を半角へ (NFKC) + strip"""
    if text is None:
        return ""
    return unicodedata.normalize("NFKC", str(text)).lower().strip()

def song_matches(song: Dict, terms: List[str]) -> bool:
    hay = " ".join([
        normalize(song.get("title", "")),
        normalize(song.get("album", "")),
        normalize(song.get("lyrics", "")),
        normalize(str(song.get("year", ""))),
        normalize(" ".join(song.get("tags", [])))
    ])
    return all(t in hay for t in terms)

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="g-kid 曲検索（Streamlit）", layout="wide")
st.markdown("<h1>g-kid 曲検索（Streamlit）</h1>", unsafe_allow_html=True)
st.write("※ローカルデータで動くデモ。`SONGS`に曲データを追加して使ってください。")

col1, col2 = st.columns([3,1])
with col1:
    q = st.text_input("検索（曲名・歌詞・アルバム・年・タグ）：", value="")
with col2:
    if st.button("クリア"):
        q = ""
        # Streamlitはここで入力を書き換えられないので再読み込み促す
        st.experimental_rerun()

# 検索処理
terms = [normalize(t) for t in q.split() if t.strip()]
if not terms:
    matched = SONGS
else:
    matched = [s for s in SONGS if song_matches(s, terms)]

st.write(f"検索結果：{len(matched)} 件")

# 結果表示（カード）
for s in matched:
    title = html.escape(s.get("title", ""))
    album = html.escape(s.get("album", ""))
    year = s.get("year", "")
    tags = s.get("tags", [])
    url = s.get("url", "#")

    card_html = f"""
    <div style="padding:12px;border-radius:10px;border:1px solid rgba(0,0,0,0.12);
                background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
                margin-bottom:8px">
      <div style="font-weight:700;font-size:16px">{title}</div>
      <div style="color:gray;margin-top:4px">{album} ・ {year}</div>
      <div style="margin-top:8px">{' '.join(f'<span style=\"display:inline-block;padding:4px 8px;border-radius:999px;border:1px solid rgba(0,0,0,0.06);margin-right:6px;font-size:12px\">{html.escape(t)}</span>' for t in tags)}</div>
      <div style="margin-top:10px;">
        <a href="{url}" target="_blank" rel="noopener">▶ プレビュー / 関連検索</a>
        &nbsp;&nbsp;
        <button onclick="navigator.clipboard.writeText('{html.escape(url)}')">リンクをコピー</button>
      </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# 追加：曲データをJSONでダウンロードするボタン
if st.button("曲データをJSONでダウンロード"):
    st.download_button("ダウンロード: songs.json", data=json.dumps(SONGS, ensure_ascii=False, indent=2), file_name="songs.json", mime="application/json")

print("はげたこちまき")