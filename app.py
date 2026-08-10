import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="3C分析アシスタント", layout="wide")

st.title("📊 3C分析自動化ツール")
st.caption("案件情報とヒアリング内容から、AIが最速で高精度な3C分析を生成します。")

# サイドバー設定
st.sidebar.header("⚙️ 設定")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Google AI Studioで取得したAPIキーを入力してください")

# 入力フォーム（タブ分けでスッキリ化）
tab1, tab2 = st.tabs(["01 案件の輪郭", "02 追加ヒアリング"])

with tab1:
    st.subheader("01 案件の輪郭を入れる（分かるところだけでOK）")
    col1, col2 = st.columns(2)
    
    with col1:
        client_name = st.text_input("クライアント名（必須）", placeholder="例：株式会社〇〇、山田 花子様")
        store_name = st.text_input("店舗名・屋号（必須）", placeholder="例：〇〇整体院、カフェ〇〇")
        service_name = st.text_input("商品・サービス名（必須）", placeholder="例：女性向けパーソナルジム")
        target_customer = st.text_input("届けたいお客さん", placeholder="例：30代後半・運動が続かない女性")
    
    with col2:
        area = st.text_input("地域・商圏", placeholder="例：横浜市、オンライン全国")
        goal = st.text_input("今回のゴール", placeholder="例：体験予約を増やしたい")
        concerns = st.text_input("気になっていること", placeholder="例：アクセスはあるのに予約されない")
    
    competitors = st.text_area("分かっている競合", placeholder="会社名、URL、参考にしたいサイトなど")

with tab2:
    st.subheader("02 お客さんに追加で聞くこと（ヒアリング）")
    q1 = st.text_area("01 いちばん売りたい商品・サービスと、その理由は？")
    q2 = st.text_area("02 いちばん届けたいお客さんは、どんな悩みを抱えていますか？")
    q3 = st.text_area("03 お客さんが比較するとき、何を基準に選びそうですか？")
    q4 = st.text_area("04 お客様の声・ビフォーアフター・実績はありますか？")
    q5 = st.text_area("05 料金・支払い方法はどうなっていますか？")
    q6 = st.text_area("06 お客さんは、知ってから申込み・購入までどんな流れですか？")
    q7 = st.text_area("07 どこまで対応できますか？（地域・人数・期間・内容など）")

st.divider()

# 分析実行ボタン
if st.button("🚀 3C分析を実行する", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ サイドバーにGemini APIキーを入力してください。")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            prompt = f"""
            以下の情報をもとに、事業の課題を整理するための3C分析をしてください。最初から特定の制作物を前提にせず、本当に必要な施策を見極めてください。

            【クライアント名】{client_name or '未入力'}
            【店舗名・屋号】{store_name or '未入力'}
            【商品・サービス】{service_name or '未入力'}
            【届けたいお客さん】{target_customer or '未入力'}
            【地域・商圏】{area or '未入力'}
            【分かっている競合】{competitors or '未入力'}
            【今回のゴール】{goal or '未入力'}
            【気になっていること】{concerns or '未入力'}

            【追加ヒアリング】
            1. 売っていきたい商品と理由: {q1 or '未入力'}
            2. お客さんの悩み: {q2 or '未入力'}
            3. 比較基準: {q3 or '未入力'}
            4. 実績・ビフォーアフター: {q4 or '未入力'}
            5. 料金・支払い方法: {q5 or '未入力'}
            6. 認知から購入までの流れ: {q6 or '未入力'}
            7. 対応範囲: {q7 or '未入力'}

            ※未入力の項目がある場合は、業界の一般的な傾向からAIで適切な「仮説」を補完して分析を進めてください。

            次の順でまとめてください。
            1. Customer：ターゲットの悩み、比較基準、欲しい未来
            2. Competitor：競合3〜5社の訴求、特徴、価格帯、使っている集客・販促方法
            3. Company：このサービスの強み・差別化できる切り口
            4. いま最優先で解くべき課題
            5. 推奨する施策と理由：LP、ホームページ、広告運用、チラシ、SNS、既存導線の改善、または別の施策を、必要性の順に提案
            6. その施策で最初に伝えるべき価値と、訴求案を3つ
            7. 追加で確認すべき質問

            「事実」と「仮説」を分け、見やすいMarkdown（表や箇条書き）でわかりやすく整理して出力してください。
            """

            with st.spinner("AIが分析中...（約10〜15秒お待ちください）"):
                response = model.generate_content(prompt)
                
            st.success("分析が完了しました！")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
