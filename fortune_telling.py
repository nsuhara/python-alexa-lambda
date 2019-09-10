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
