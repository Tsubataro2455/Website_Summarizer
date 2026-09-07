# Website Summarizer 🤗

Webサイトのコンテンツを自動的に取得し、Claude AIを使用して日本語で簡潔に要約するアプリケーションです。

## ✨ 機能

- **URL入力による自動要約**: URLを入力するだけでWebサイトの内容を日本語で要約
- **リアルタイムストリーミング表示**: Claude の応答がリアルタイムで表示されるため、待ち時間を短縮
- **複数のモデル対応**: Claude Haiku 4.5（高速・低コスト）と Claude Sonnet 4.6（高精度）から選択可能
- **API使用コスト追跡**: 各要約のコストを計算し、合計使用量をサイドバーに表示
- **会話履歴管理**: 複数のWebサイト要約をまとめて処理し、クリアボタンで履歴をリセット可能

## 🚀 クイックスタート

### 前提条件

- Python 3.11以上
- Anthropic API キー（[https://console.anthropic.com](https://console.anthropic.com)から取得）

### インストール

#### ローカル環境での実行

```bash
# リポジトリをクローン
git clone <repository-url>
cd website_sammaty

# 依存パッケージをインストール
pip install -r requirements.txt

# 環境変数を設定
export ANTHROPIC_API_KEY="your-api-key-here"

# アプリを起動
streamlit run src/main.py
```

ブラウザで `http://localhost:8501` を開いてアプリにアクセスします。

#### Dockerでの実行

```bash
# .envファイルを作成してAPIキーを設定
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env

# Docker Composeで起動
docker-compose up --build
```

ブラウザで `http://localhost:8501` を開いてアプリにアクセスします。

## 📖 使い方

1. **サイドバーでモデルを選択**
   - Claude Haiku 4.5: 高速で低コスト（テキスト重視のコンテンツ向け）
   - Claude Sonnet 4.6: より精度の高い要約（複雑なコンテンツ向け）

2. **URLを入力**
   - テキストボックスにWebサイトのURLを入力（例: https://example.com）

3. **要約を表示**
   - アプリが自動的にコンテンツを取得し、日本語で要約を生成します
   - 要約と元のテキストが表示されます

4. **コスト確認**
   - サイドバーの「Costs」セクションで、API使用に伴うコストをドル単位で確認できます

5. **会話をクリア**
   - 「Clear Conversation」ボタンをクリックして、履歴とコストをリセット

## 💰 API コスト

Claude APIの価格（2025年9月時点）:

| モデル | 入力トークン | 出力トークン |
|--------|------------|-----------|
| Claude Haiku 4.5 | $0.80/百万 | $4.00/百万 |
| Claude Sonnet 4.6 | $3.00/百万 | $15.00/百万 |

アプリは自動的に使用トークン数を計算し、リアルタイムでコストを表示します。

## 🏗️ 技術スタック

- **フロントエンド**: [Streamlit](https://streamlit.io/) 1.63.0
- **LLMフレームワーク**: [LangChain](https://www.langchain.com/) 1.4.0
- **LLMモデル**: [Claude API](https://www.anthropic.com/)（via langchain-anthropic）
- **Webスクレイピング**: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) 4.15.0
- **HTTPクライアント**: [requests](https://requests.readthedocs.io/) 2.34.2
- **コンテナ化**: Docker、Docker Compose

## 📋 システム要件

- Python 3.11以上
- メモリ: 512MB以上（推奨: 1GB以上）
- ネットワーク接続（Claude APIへのアクセス）

## 🔧 カスタマイズ

### 要約の言語変更

`src/main.py` の `build_prompt()` 関数を編集してください：

```python
def build_prompt(content, n_chars=300):
    return f"""以下はとあるWebページのコンテンツである。内容を{n_chars}程度でわかりやすく要約してください。
    
    # ここを変更して他の言語にも対応
    """
```

### 要約文字数の調整

`src/main.py` の118行目で、デフォルト文字数を変更できます：

```python
prompt = build_prompt(content, n_chars=500)  # 500文字に変更
```

### コンテンツ抽出の改善

一部のWebサイトでは、ページ構造により正しくコンテンツが抽出されない場合があります。`get_content()` 関数を編集して、特定のサイト向けにカスタマイズできます。

## ⚠️ 注意点

- このアプリは、スクレイピング対象のWebサイトの利用規約を確認した上で使用してください
- Cloudflareなどの保護機能を備えたサイトは、スクレイピングが失敗する可能性があります
- JavaScriptで動的に生成されるコンテンツには対応していません
- セッション状態は再読み込みでリセットされます（コストデータを永続化する場合は、データベースの統合が必要です）

## 🐛 トラブルシューティング

### エラー: "ANTHROPIC_API_KEY not found"

APIキーが正しく設定されていません：

```bash
# Linux/Mac
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

### コンテンツが取得できない

以下を確認してください：
- URLが有効か
- サイトがスクレイピングを許可しているか
- `<main>`, `<article>`, `<body>` タグがページに存在するか

### ストリーミング表示が遅い

- より軽量な Claude Haiku 4.5 モデルを試してみてください
- ネットワーク接続を確認してください

## 📝 ファイル構成

```
website_sammaty/
├── README.md                 # このファイル
├── CLAUDE.md                 # Claude Code用ドキュメント
├── Dockerfile                # Docker イメージ定義
├── docker-compose.yml        # Docker Compose 設定
├── requirements.txt          # Python依存パッケージ
├── .env                       # 環境変数（APIキー等）
├── .gitignore                # Git 無視ファイル設定
└── src/
    └── main.py               # メインアプリケーション
```

## 🚧 今後の改善予定

- [ ] 複数言語への対応
- [ ] 要約精度の向上
- [ ] Markdown形式での出力
- [ ] コスト履歴のデータベース保存
- [ ] キャッシング機能
- [ ] バッチ処理（複数URLの一括要約）
- [ ] ダークモード対応

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🤝 貢献

バグ報告、機能リクエスト、プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## 📧 サポート

問題が発生した場合は、GitHubのissueセクションで報告してください。

---

**Made with ❤️ using Claude API and Streamlit**
