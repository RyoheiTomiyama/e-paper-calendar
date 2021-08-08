# e-paper-calendar

ラズパイと電子ペーパーを使って、予定とカレンダー、天気情報を表示させる。

![800x480](https://user-images.githubusercontent.com/10805686/128620971-50f196a5-ccc1-4d90-8308-a5297bef9441.png)

## Dependency

- [RaspberryPI Zero WH](https://a.r10.to/hyr7lN)
- [電子ペーパー　waveshare 7.5inch HAT (B)](https://amzn.to/3rY5dLq)
- Poetry
- Python^3.8

## Setup

以下の作業は、ラズパイに入れる前にパソコンから行って下さい。

### GoogleカレンダーにアクセスするためのGCPアプリの作成と認証情報の作成

1. GCPアプリを作成
1. Google Calendar API を有効にしておく
1. OAuthクライアントID(デスクトップアプリ)を作成
1. jsonをダウンロードして、credentials.jsonにリネームして、./oauthディレクトリに格納

OAuth同意画面の公開ステータスを本番環境にしないと、7日間で認証切れになってしまうので注意

### OpenWeatherAPIキーの取得

以下のページからアカウント登録（無料で利用できます）
https://home.openweathermap.org/users/sign_up

登録したらMy API Keysから、Keyをコピー
`.env`ファイルをルートディレクトリに作成

```sh
OPEN_WEATHER_API_KEY=$YOUR_API_KEY
```

### 天気情報を取得したい軽度緯度を設定

https://openweathermap.org/find
OpenWeatherのサイトから取得したい場所を検索（英語で検索すると良い）

検索結果から得た軽度緯度を.envに追加

```sh
LATITUDE=$YOUR_CITY_LAT
LONGITUDE=$YOUR_CITY_LONG
```

### テスト実行（Google認証を通す）

`main.py`の`IS_LOCAL=True`のコメントアウトを外す

```python
# 開発中に画像を書き出してテストしたいときは、コメントアウトを外す
IS_LOCAL = True   # <---ここのコメントアウトを外す
```

```sh
$ poetry install
$ poetry run python main.py
```

実行すると、Google認証のためにブラウザが開かれる  
カレンダー情報を取得したいアカウントでログイン

認証完了したら、`oath/token.json`が作成されている  
ブラウザは閉じて大丈夫です

実行が正常に終了したら、`output/｀に電子ペーパーに表示したい画像が生成されていれば成功

## Usage

続いてラズパイでの使い方

ラズパイに接続
```sh
$ ssh raspi
```

### Poetryのインストール

```sh
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

$ vim ~/.bashrc
# 1行追加
PATH=$HOME/.poetry/bin:$PATH;

$ source ~/.bashrc

$ poetry --version
Poetry version 1.1.7
```

(公式にある`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -`だと上手く行かなかった)


### Setupで作業したデータをラズパイに入れる

```sh
$ git clone https://github.com/RyoheiTomiyama/e-paper-calendar
$ cd e-paper-calendar
```

Setupで作成した`credentials.json` `token.json` `.env`等 を追加する

```sh
$ scp -r ./oauth/ raspi:~/e-paper-calendar/oauth/
$ scp -r ./.env raspi:~/epaper/e-paper-calendar/.env
$ scp -r Fonts/ raspi:~/epaper/e-paper-calendar/Fonts/
```


### インストール


```bash
$ sudo apt-get install --fix-missing python3-dev python3-setuptools libjpeg-dev
$ pip install Pillow
```

`--fix-missing`を付けないと`Cannot initiate the connection to [raspbian.raspberrypi.org](http://raspbian.raspberrypi.org/)` になった。

```sh
$ poetry install

# ラズパイだけで使うパッケージのインストール
$ poetry shell
.venv > $ pip intall spidev
.venv > $ pip install rpi.gpio
```

### Cronの設定

`cron.sh`を実行できるように権限を変更

```sh
$ chmod 777 ./cron.sh
```

エラーログを入れておくファイルを作成
```sh
$ sudo touch /var/log/e-calendar.log
$ sudo chmod 666 /var/log/e-calendar.log
```

cron設定
```sh
$ crontab -e
# メール送信不要なので
MAILTO=""

# 電子ペーパー 1時間ごとに実行
0 * * * * sh /home/pi/epaper/e-paper-calendar/cron.sh > /var/log/e-calendar.log 2>&1
```
