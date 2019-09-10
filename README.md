# AlexaスキルをPython/Lambdaで実装する

- [AlexaスキルをPython/Lambdaで実装する](#alexa%e3%82%b9%e3%82%ad%e3%83%ab%e3%82%92pythonlambda%e3%81%a7%e5%ae%9f%e8%a3%85%e3%81%99%e3%82%8b)
  - [はじめに](#%e3%81%af%e3%81%98%e3%82%81%e3%81%ab)
    - [目的](#%e7%9b%ae%e7%9a%84)
    - [関連する記事](#%e9%96%a2%e9%80%a3%e3%81%99%e3%82%8b%e8%a8%98%e4%ba%8b)
    - [実行環境](#%e5%ae%9f%e8%a1%8c%e7%92%b0%e5%a2%83)
    - [ソースコード](#%e3%82%bd%e3%83%bc%e3%82%b9%e3%82%b3%e3%83%bc%e3%83%89)
  - [事前準備](#%e4%ba%8b%e5%89%8d%e6%ba%96%e5%82%99)
    - [Amazon Developerアカウントの作成](#amazon-developer%e3%82%a2%e3%82%ab%e3%82%a6%e3%83%b3%e3%83%88%e3%81%ae%e4%bd%9c%e6%88%90)
    - [AWSアカウントの作成](#aws%e3%82%a2%e3%82%ab%e3%82%a6%e3%83%b3%e3%83%88%e3%81%ae%e4%bd%9c%e6%88%90)
    - [skill.zipの作成](#skillzip%e3%81%ae%e4%bd%9c%e6%88%90)
  - [Alexaスキルの作成](#alexa%e3%82%b9%e3%82%ad%e3%83%ab%e3%81%ae%e4%bd%9c%e6%88%90)
  - [AWS Lambdaの構築](#aws-lambda%e3%81%ae%e6%a7%8b%e7%af%89)
  - [Alexaスキルのテスト](#alexa%e3%82%b9%e3%82%ad%e3%83%ab%e3%81%ae%e3%83%86%e3%82%b9%e3%83%88)

## はじめに

Mac環境の記事ですが、Windows環境も同じ手順になります。環境依存の部分は読み替えてお試しください。

### 目的

この記事を最後まで読むと、次のことができるようになります。

- Alexaスキルを作成する
- AWS Lambdaを構築する

`Alexaシミュレータ`

<img width="400" alt="スクリーンショット 2019-09-09 21.08.01.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/47ba76ed-747f-ab34-8179-32f15095ba5f.png">

### 関連する記事

- [Amazon Alexa](https://developer.amazon.com/ja/alexa)
- [AWS](https://aws.amazon.com/jp/)
- [Alexa Skills Kit SDK for Python](https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/index.html)

### 実行環境

| 環境         | Ver.    |
| ------------ | ------- |
| macOS Mojave | 10.14.6 |
| Python       | 3.7.3   |
| ask-sdk      | 1.11.0  |

### ソースコード

実際に実装内容やソースコードを追いながら読むとより理解が深まるかと思います。是非ご活用ください。

[GitHub](https://github.com/nsuhara/python-alexa-lambda.git)

## 事前準備

### Amazon Developerアカウントの作成

[Amazon Alexa](https://developer.amazon.com/ja/alexa)の`ログイン`からAmazon Developerアカウントを作成する

### AWSアカウントの作成

[AWS](https://aws.amazon.com/jp/)の`コンソールにサインイン`からAWSアカウントを作成する

### skill.zipの作成

```tree.sh
pj_folder
└── fortune_telling.py
```

```fortune_telling.py
import random

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import get_slot_value, is_intent_name, is_request_type
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

sb = SkillBuilder()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "今日の運勢を占いますか? (はい/いいえ)"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Fortune Telling", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("FortuneTellingIntent"))
def fortune_telling_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    yes_no = get_slot_value(handler_input=handler_input, slot_name="continue")
    if yes_no == 'はい':
        num = random.randint(0, 9)
        if num >= 0 and num <= 2:
            speech_text = "大吉ですねっ!ホッとした。"
        elif num >= 3 and num <= 6:
            speech_text = "小吉かぁ。微妙な1日。"
        else:
            speech_text = "大凶ですよ。はい残念!"
        speech_text = '{} 続けますか? (はい/いいえ)'.format(speech_text)
        end_session = False
    elif yes_no == 'いいえ':
        speech_text = "ほな、さいならー"
        end_session = True
    else:
        speech_text = "えっなんて?"
        end_session = False

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Fortune Telling", speech_text)).set_should_end_session(end_session)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "こんにちは。と言ってみてください。"

    handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
        SimpleCard("Fortune Telling", speech_text))
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "さようなら"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Fortune Telling", speech_text))
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    # type: (HandlerInput) -> Response

    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # type: (HandlerInput, Exception) -> Response
    print(exception)

    speech = "すみません、わかりませんでした。もう一度言ってください。"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


handler = sb.lambda_handler()
```

```skill.sh
cd pj_folder
mkdir skill
cd skill
cp fortune_telling.py skill/
pip install ask-sdk-core -t .
zip ../skill.zip -r .
```

```tree.sh
pj_folder
├── fortune_telling.py
├── skill
└── skill.zip
```

## Alexaスキルの作成

1. 占いスキル(FortuneTelling)を作成する

    Alexa Developer Consoleを開く > `スキルの作成`をクリック

    <img width="700" alt="スクリーンショット 2019-09-09 19.50.25.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/c70a3dee-6eb0-d1d7-af15-5e5e8da0f081.png">

    以下を入力/選択して`スキルの作成`をクリック
    - スキル名に`FortuneTelling`を入力
    - スキルに追加するモデルを選択で`カスタム`を選択
    - スキルのバックエンドリソースをホスティングする方法を選択で`ユーザー定義のプロビジョニング`を選択

    <img width="700" alt="スクリーンショット 2019-09-09 19.51.07.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/a90c4fc7-fb07-e8d7-e84c-a081a728d456.png">

2. 呼び出し名を設定する

    呼び出し名に`占いくん`を入力

    <img width="700" alt="スクリーンショット 2019-09-09 20.02.32.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/d425c0b1-fa3b-9e94-da1b-cafb6f518d30.png">

3. スロットタイプを作成する

    `スロットタイプ`をクリック > スロットタイプに`continueType`を入力 > `カスタムスロットタイプを作成`をクリック

    スロット値に`はい`と`いいえ`を追加

    <img width="700" alt="スクリーンショット 2019-09-09 20.08.41.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/b611ec40-e5b7-f1f3-6d48-44505a7a5306.png">

4. インテントを作成する

    `インテントを追加`をクリック > `FortuneTellingIntent`を入力 > `カスタムインテントを作成`をクリック

    インテントスロットに`continue`を追加 > スロットタイプに`continueType`を入力

    <img width="700" alt="スクリーンショット 2019-09-09 20.16.09.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/7c757574-d412-07e2-b6e8-9cf9400cffd9.png">

    サンプル発話に`{continue}`を追加

    <img width="700" alt="スクリーンショット 2019-09-09 20.19.11.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/60fe6a46-7a13-2a25-b3d9-6aa65a1c7990.png">

5. JSONエディターで設定内容を確認する

    ```json_editor.json
    {
        "interactionModel": {
            "languageModel": {
                "invocationName": "占いくん",
                "intents": [
                    {
                        "name": "AMAZON.CancelIntent",
                        "samples": []
                    },
                    {
                        "name": "AMAZON.HelpIntent",
                        "samples": []
                    },
                    {
                        "name": "AMAZON.StopIntent",
                        "samples": []
                    },
                    {
                        "name": "AMAZON.NavigateHomeIntent",
                        "samples": []
                    },
                    {
                        "name": "FortuneTellingIntent",
                        "slots": [
                            {
                                "name": "continue",
                                "type": "continueType"
                            }
                        ],
                        "samples": [
                            "{continue}"
                        ]
                    }
                ],
                "types": [
                    {
                        "name": "continueType",
                        "values": [
                            {
                                "name": {
                                    "value": "いいえ"
                                }
                            },
                            {
                                "name": {
                                    "value": "はい"
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }
    ```

## AWS Lambdaの構築

1. 関数を作成する

    AWS マネジメントコンソールを開く > サービスをクリック > Lambdaをクリック > `関数の作成`をクリック

    オプションで`一から作成`を選択 > 関数名に`FortuneTelling`を入力 > ランタイムで`Python 3.7`を選択 > `関数の作成`をクリック

    <img width="700" alt="スクリーンショット 2019-09-09 20.28.55.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/cb20bdb4-742d-4d0b-7257-187ecc1082c3.png">

1. トリガーを設定する

    作成したスキルのエンドポイントを開く > AWS LambdaのARNをクリック > `スキルID`をコピー

    <img width="700" alt="スクリーンショット 2019-09-09 20.31.39.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/fadd2f6e-1318-89c5-4e5a-a6852cfba192.png">

    作成した関数の`トリガーを追加`をクリック > トリガーを選択で`Alexa Skills Kit`を選択 > スキルID検証で`有効`を選択 > スキルIDに先ほどコピーした`スキルID`を入力 > `追加`をクリック

    <img width="700" alt="スクリーンショット 2019-09-09 20.37.15.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/14e96bd3-35e1-8031-67fe-31d7aab9903a.png">

1. 関数コードを設定する

    ブラウザを更新 > コード エントリ タイプで`.zip ファイルをアップロード`を選択 > アップロードをクリック > 事前に準備した`skill.zip`を選択 > ハンドラに`fortune_telling.handler`を入力 > `保存`をクリック

    <img width="700" alt="スクリーンショット 2019-09-09 20.54.31.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/62cea9b6-da3d-1464-09d0-f097fab95422.png">

1. エンドポイントを設定する

    作成した関数のARNをコピー

    <img width="700" alt="スクリーンショット 2019-09-09 20.58.09.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/f8fa943a-b6cd-5541-3dd5-d3c141ad9fed.png">

    作成したスキルのエンドポイントを開く > AWS LambdaのARNをクリック > デフォルトの地域に先ほどコピーした`ARN`を入力 > `エンドポイントを保存`をクリック

    <img width="700" alt="スクリーンショット 2019-09-09 21.02.24.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/d74af228-035d-e630-1a27-dc7b833e8b94.png">

1. モデルをビルドする

    `モデルを保存`をクリック > `モデルをビルド`をクリック

    <img width="700" alt="スクリーンショット 2019-09-09 21.04.34.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/dbeb0956-24d9-34ad-ec17-571c278400b5.png">

## Alexaスキルのテスト

テストをクリック > `開発中`をクリック > `占いくん`を入力 > `はい` or `いいえ`を入力

<img width="400" alt="スクリーンショット 2019-09-09 21.08.01.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/47ba76ed-747f-ab34-8179-32f15095ba5f.png">
