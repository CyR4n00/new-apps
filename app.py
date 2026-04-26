import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import time

# --- モックデータの生成 ---
@st.cache_data
def generate_mock_data():
    dates = [datetime.now() - timedelta(days=i) for i in range(14)]
    data = []
    topics = ["マーケティング", "AIツール活用", "Pythonプログラミング", "副業の始め方", "日常の気づき", "SEO対策", "SNS運用術"]
    for d in dates:
        views = random.randint(100, 5000)
        likes = int(views * random.uniform(0.01, 0.1))
        replies = int(likes * random.uniform(0.05, 0.3))
        topic = random.choice(topics)
        text = f"【保存版】{topic}で失敗しないコツをまとめました。実は多くの方が..."

        data.append({
            "選択": True, # データエディタ用のチェックボックス
            "日付": d.strftime("%Y-%m-%d"),
            "トピック": topic,
            "投稿テキスト": text,
            "表示回数": views,
            "いいね": likes,
            "エンゲージ率(%)": round((likes + replies) / views * 100, 2)
        })
    return pd.DataFrame(data)

# --- Streamlit アプリのUI構築 ---

st.set_page_config(page_title="Threads運用アシスタント", layout="wide")

st.title("🧵 Threads 運用アシスタント (パーソナライズ＆Agent版)")

# サイドバー: アカウント連携とパーソナライズ設定
st.sidebar.header("アカウント連携")
account_status = st.sidebar.selectbox("連携アカウント", ["@your_account", "新規連携..."])

st.sidebar.markdown("---")
st.sidebar.header("👤 ペルソナ＆トーン設定")
st.sidebar.caption("AIにあなた（またはクライアント）のキャラを学習させます")
persona = st.sidebar.text_area("あなたのアカウントのキャラ・強み", value="データ分析が得意なマーケター。論理的だが、初心者に寄り添う優しい口調。")
target_audience = st.sidebar.text_area("ターゲット層", value="SNS運用で疲弊している個人事業主や、効率化したいフリーランス。")
tone = st.sidebar.selectbox("文体（トーン＆マナー）", ["親しみやすい（絵文字多め）", "ビジネスライク（説得力重視）", "ポエム調（共感重視）", "Hermes Agent (自律思考的)"])

st.markdown("---")

tab1, tab2 = st.tabs(["📊 データ分析＆学習データの選択", "✨ AI投稿生成＆プロンプト調整"])

df = generate_mock_data()

with tab1:
    st.subheader("分析結果とAIに読み込ませるデータの選択")
    st.write("過去の投稿から、AIに「成功例（Few-shot）」として学習させるデータを選択・編集できます。")

    col1, col2, col3 = st.columns(3)
    col1.metric("総表示回数", f"{df['表示回数'].sum():,}")
    col2.metric("総いいね数", f"{df['いいね'].sum():,}")
    col3.metric("平均エンゲージ率", f"{df['エンゲージ率(%)'].mean():.1f}%")

    # st.data_editorでデータを直接編集・選択可能にする
    edited_df = st.data_editor(
        df,
        column_config={
            "選択": st.column_config.CheckboxColumn("AIに学習させる", help="チェックを入れた投稿がプロンプトの参考データとしてAIに送られます", default=True),
        },
        disabled=["日付", "表示回数", "いいね", "エンゲージ率(%)"],
        hide_index=True,
        use_container_width=True
    )

with tab2:
    st.subheader("プロンプト（指示書）の可視化とカスタマイズ")

    target_topic = st.text_input("📝 今回作成したい投稿のテーマ（キーワード）を入力:", value="AIツールを使った業務効率化")

    # 選択されたデータだけを抽出
    selected_data = edited_df[edited_df["選択"] == True]
    reference_texts = "\n".join([f"- {row['投稿テキスト']} (エンゲージ率: {row['エンゲージ率(%)']}%)" for _, row in selected_data.head(3).iterrows()])

    # 動的にプロンプトを構築
    raw_prompt = f"""あなたは優秀なSNSマーケティングエージェント（Hermes Agent）です。
以下の前提条件と過去の成功データを分析し、最もエンゲージメントが高まるThreadsの投稿を作成してください。

【前提条件】
- アカウントのキャラ: {persona}
- ターゲット層: {target_audience}
- 文体: {tone}
- 今回のテーマ: {target_topic}

【過去の成功投稿（参考データ）】
{reference_texts if reference_texts else "（データなし）"}

【指示】
1. なぜこの構成にしたのか（思考プロセス）を簡潔に出力してください。
2. 実際に投稿するテキスト案（500文字以内）を1つ出力してください。
"""

    with st.expander("🛠️ 送信されるシステムプロンプト（直接編集可能）", expanded=True):
        final_prompt = st.text_area("以下の内容がAI（Hermes等のLLM）に送信されます。自由に書き換えて調整できます。", value=raw_prompt, height=350)

    if st.button("🚀 Agentに投稿を生成させる", type="primary"):
        with st.spinner("Hermes Agent がデータを分析・思考中..."):
            time.sleep(2) # API通信のモック

            # Agent風の出力モック
            st.markdown("### 🧠 Agentの思考プロセス")
            st.info("過去の成功データを見ると、「失敗しないコツ」や「保存版」といったキーワードのエンゲージ率が高い傾向にあります。ターゲットであるフリーランスは「時間を無駄にしたくない」というペインを抱えているため、今回は『AIツール選びで失敗しないための基準』を提示し、論理的かつ共感を呼ぶ構成にします。")

            st.markdown("### 📝 生成された投稿案")
            st.success(f"""【保存版】AIツール、適当に選んでませんか？🤖\n\n「とりあえず話題のAIを使ってみたけど、結局元のやり方に戻った…」\nフリーランスの方から、そんな悩みをよく聞きます。\n\nAIツール導入で失敗しないコツは、ズバリ「自分の業務の"どこ"を代替させるか」を最初に定義すること。\n\n1. 情報収集（リサーチ）\n2. テキスト作成（ドラフト）\n3. データ分析\n\n全部をAIに任せるのではなく、自分が一番時間がかかっている1つの工程だけをAIに置き換えるのが成功の近道です💡\n\n皆さんはどの作業をAIに任せたいですか？リプ欄で教えてください👇\n\n#業務効率化 #{target_topic} #フリーランスの日常""")
