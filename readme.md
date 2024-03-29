FastAPI-実用的テンプレート
====
FastAPIを使用した実用的なテンプレートです。
DB(MySQL)とuvicornを含めてdocker化しています。
poetryを使用して、パッケージ管理およびタスクランナーを実装しています。

# デモ環境(heroku)
本リポジトリに、herokuにデプロイするための設定ファイルも含まれております。<br>
デプロイ済の環境は以下から参照できます。
```
https://fastapi-sample-tk.herokuapp.com/docs
```

DB定義(dbdocs)
```
https://dbdocs.io/marutoraman/fastapi-sample?table=jobs&schema=public&view=table_structure
```

# 機能(Features)

## DBレコードの作成・取得・更新・削除(CRUD)
crud/base.py にCRUDの共通Classを記述しています。
それ以外のcrud配下のファイルで、CRUD処理をoverrideすることができます。

## 権限(scopes)
特定のUserのみが実行できるAPIを作成する場合は、
tableの user.scopes の値とrouterに指定したscopeを一致させる。

```
@router.get(
    "/{id}",
    response_model=schemas.UserResponse,
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
```

## キャメルケースとスネークケースの相互変換
Pythonではスネークケースが標準ですが、Javascriptではキャメルケースが標準なため、単純にpydanticでschemaを作成しただけでは
jsonレスポンスにスネークケースを使用せざるをえない問題があります。

そこで、humpsをinstallして、自動的にスネークケースに変換するように
以下のようなBaseSchemaを作成しています。
このBaseSchemaを継承することで、簡単にキャメルケースとスネークケースの相互変換が実現できます。

```
class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
```

## バッチ処理(batch)
サブディレクトリ配下のpyファイルから、別ディレクトリのファイルをimportする場合は
その前に以下のコードを記述する必要がある。

```
sys.path.append(str(Path(__file__).absolute().parent.parent))
```

batch/__set_base_path__.py に記述し、各ファイルの先頭でimportすることで
より簡単にimportできるようにしています。


## Settings
BaseSettingsを継承して共通設定Classを作成している。
.envファイルから自動的に設定を読み込む他、個別に設定を定義することもできる。

## ErrorException
exceptions/error_messages.py にエラーメッセージを定義している。
APIExceptionと併せて以下のように、呼び出すことで、エラーレスポンスを作成できる。
```
raise APIException(ErrorMessage.ID_NOT_FOUND)
```

## logging
logger_config.yaml から設定を読み込む。

## テスト
tests/ 配下に、テスト関連の処理を、まとめている。

テスト関数の実行毎にDBをクリーンするため、ステートレスなテストが実行できます。
tests/test_data/ 配下にテスト用データをセットする。

## ログの集中管理
.envファイルにsentryのDNSを設定すると、error以上のloggingが発生した場合に
sentryに自動的にloggingされます。

## DBマイグレーション
alembic/versions.py にマイグレーション情報を記述すると、DBマイグレーション(移行)を実施することができます。


## パッケージ管理
poetryを使用して、パッケージ管理を実施。
また、poethepoetを使用するすることでタスクランナー機能を追加している。


## CI/CD
push時に、Github Actionsを使用して、ECSに自動デプロイを行います。
以下にAWSの設定情報等をセットします。
.aws/ecs-task-definition.json
.github/workflow/aws.yml

# インストール&使い方(Installations & How to use)

## Dockerコンテナ内で開発(推奨)

### VSCODEに「Remote Containers」をインストール
拡張機能「Remote Containers」をインストール

### コンテナを起動
コマンドパレットを開き、「reopen container」と入力して実行

### コンテナ内のコンソールログ確認方法
リモートエクスプローラー -> CONTAINERS -> {{ コンテナ名 }} -> Show Container Logs　

## ローカルで開発
ローカルで開発する場合
### Poetryのインストール
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### 依存パッケージのインストール
```
poetry install
```

### dockerコンテナのビルド & 起動
```
docker-compose up --build
```

## API管理画面(OpenAPI)表示
ローカル環境
```
http://localhost:8090/docs
```

Debugモード(F5押下)で起動した場合
※Debugモードの場合は、ブレークポイントでローカル変数を確認できます。
```
http://localhost:8091/docs
```

## poeタブ入力補完設定(completion)
※dockerコンテ内で開発する場合は、Dockerfileに組み込まれているため実行不要です
bashを使用している場合は、以下のコマンドを実行する。<br>
これにより、タスクランナー実行時にタブで入力補完が可能になります。<br>

```bash
 poe _bash_completion >> ~/.bashrc
```

次回bash起動時に有効化されるが、即時有効化するためには以下を実行する。
```
. ~/.bashrc
```we

# デプロイ
heroku-cliを使用したherokuへのデプロイ方法を説明します。

## heroku-cliのインストール
以下を参考にインストール<br>
https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli

## appの作成
APPNAMEは任意の名称を指定（全ユーザーでユニークである必要があります）
```
heroku create APPNAME
```

## gitにherokuのリモートリポジトリをセット
```
heroku git:remote --app APPNAME
```

## push
```
git push heroku master
```

## heroku-cliにheroku-configをインストール
本リポジトリでは、.envファイル経由で設定を読み込んでいるため<br>
herokuでも.envファイルを有効にする必要があります。<br>
```
heroku plugins:install heroku-config
```

## .envファイルをpush
```
heroku config:push
```

## heroku再起動
```
heroku restart
```
