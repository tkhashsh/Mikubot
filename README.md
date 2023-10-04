# Mikubot

VLL Discord サーバーのためのBot

~~TOKEN等はGithub ActionsのSecretsに格納しDockerでBuildする際に環境変数に加えています。~~

イメージに焼き付けたくなかったので実行時に`--env`オプションで渡してます。

## v2の変更点

<details open>
<summary>利用者向け</summary>

### メッセージURLの展開ができます

VLL Discord内のBotに閲覧権限があるチャンネルのメッセージURLを送信すると、そのメッセージの内容を展開して表示します。

Botが見れさえすれば、たとえばVLL DiscordからKAFUECサーバー上のメッセージの展開もできます。

### 誰でもピン留めを利用できます

ピン留めしたいメッセージを右クリック(PC) or 長押し(スマホ)して「Pin / Unpin」を選択すると、

- そのメッセージがピン留めされていない場合はピン留めします。
- そのメッセージがピン留めされている場合はピン留めを解除します。

### 投票コマンドが新しくなりました

すべての投票が`/vote`コマンドに統合されて、最大20個の選択肢を投票できるようになりました。また、投票の集計も手軽になりました。詳しくは`/help`から参照してください。これに伴って、投票がタイムアウトした際に自動で集計する機能が削除されています。今後は明示的に集計を行ってください。ご迷惑をおかけします。

⚠️ 集計コマンドには比較的最近Discordに追加された機能が使用されています。もし利用できない場合はクライアントの更新をお試しください。

### Timetree

TimeTreeAPIが2023年12月22日に廃止されることが判明したので、Timetreeの機能は削除されました。ご迷惑をおかけします。

### リマインダー(後日追加予定)

日時を設定して事前に設定したメンションなどを飛ばせるようにします。

**締切を守ろう！！！！！！！**

</details>

<details>
<summary>開発者向け</summary>

### `poetry`と`pre-commit`を使用するようになりました

pipではなくpoetryを使用するようになりました。また、pre-commitを使用して
デプロイ用`requirements.txt`の自動生成を行うようになりました。

```bash
git clone <this repo>
cd <this repo>
poetry install
poetry run pre-commit install
```

### 依存ライブラリを更新しました

`discord.py v1.7.3`及び`dislash.py`は今後利用できなくなる可能性があるため、`discord.py v2`ベースですべて書き直しました。

### ファイル分割

単一ファイルにすべての処理が書かれていたものを[Cog and Extension](https://discordpy.readthedocs.io/ja/latest/ext/commands/extensions.html)ベースのファイル分割に変更しました。

起動時にファイル探索をし、**app/\*\*/cog.py** というファイル名のExtensionが自動で読み込まれます。

### スニペット

VSCode向けの新規Cog作成スニペットを追加してあります。

### CI

- `pre-commit`を使用して、基本的なコードチェックを行っています。`requirements.txt`の更新を忘れるとCIが失敗します。
  - Pull Request内であれば修正を自動でコミットしてくれます。
- Dockerイメージのビルドまでを事前にテストしています。(起動確認はしていません)
- typoチェッカーも回しています。

### ビルド・デプロイ

GitHub Actionsでイメージをビルドして、現在VLL Wikiなどを稼働させているConoHa VPS上へ
自動デプロイする設定になっています。

### 謎のライブラリ(experimental)

`components/ui`以下に実験的な謎のUIライブラリがあります。
ボタンなどを含むコンポーネントを宣言的に書けてReactのような状態更新もできます。

型にも配慮されていて、静的型チェックはもちろんのこと、一部は実行時にAPIリクエストの手前で型チェックをしています。IDEの補完も効きやすいように作っています。

今後少しずつ独自ライブラリとして切り出して最終的にはどこかに公開したいな

```py
class TestView(View):
    def __init__(self) -> None:
        self.count = State(0, self)
        super().__init__()

    def export(self) -> ViewObject:
        async def increment(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x + 1)

        async def decrement(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x - 1)

        async def reset(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(0)

        e = discord.Embed(
            title="Count",
            description=f"Count: {self.count.get_state()}",
        )

        return ViewObject(
            embeds=[e],
            components=[
                Button("+1", style={"color": "green"}, on_click=increment),
                Button("-1", style={"color": "red"}, on_click=decrement),
                Button(
                    "Reset",
                    style={
                        "color": "blurple",
                        "emoji": "🔄",
                        "disabled": self.count.get_state() == 0,
                    },
                    on_click=reset,
                ),
            ],
        )
```

</details>
