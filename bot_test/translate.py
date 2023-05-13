# -*- encoding: utf-8 -*-

"""
@File    : google_tranaslate.py
@Time    : 2022/7/21
@Author  : L_W_D
@Description: -
"""
import json
import typing

import requests
import unicodedata


class GoogleTranslate(object):
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl={sl}&tl={tl}&q={q}"
    language_list = ["en", "zh-CN","ja"]
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    sesssion = requests.Session()

    @classmethod
    def deal_punctuation(cls, text: str) -> str:
        """
        中文标点符号转英文
        :param text:原文本
        :return:
        """
        return_text = unicodedata.normalize("NFKC", text)
        return return_text

    @classmethod
    def __send_requests(cls, source: str, target: str, text: str) -> str:
        text = cls.deal_punctuation(text)
        url = cls.url.format(sl=source, tl=target, q=text)
        response = cls.sesssion.get(url=url)
        return response.text

    @classmethod
    def en2cn(cls, text: str) -> typing.Tuple[bool, str]:
        """
        英文 ->中文
        :param text: 需要翻译的文本
        :return: tuple(bool:是否翻译成功 str:翻译结果)
        """
        source = "en"
        target = "zh-CN"
        text = text.title()
        response_text = cls.__send_requests(source=source, target=target, text=text)
        if "Error 400 (Bad Request)!!" in response_text:
            return False, ""
        try:
            bak_json = json.loads(response_text)
            return_text = bak_json[0][0][0]
            return_text = cls.deal_punctuation(return_text)
            return True, return_text
        except Exception as e:
            return False, ""

    @classmethod
    def cn2en(cls, text: str) -> typing.Tuple[bool, str]:
        """
        中文->英文
        :param text: 需要翻译的文本
        :return: tuple(bool:是否翻译成功 str:翻译结果)
        """
        source = "zh-CN"
        target = "en"
        response_text = cls.__send_requests(source=source, target=target, text=text)
        try:
            bak_json = json.loads(response_text)
            return_text = bak_json[0][0][0]
            return_text = cls.deal_punctuation(return_text)
            return True, return_text
        except Exception as e:
            return False, ""

    @classmethod
    def ja2en(cls, text: str) -> typing.Tuple[bool, str]:
        """
        日文->英文
        :param text: 需要翻译的文本
        :return: tuple(bool:是否翻译成功 str:翻译结果)
        """
        source = "ja"
        target = "en"
        response_text = cls.__send_requests(source=source, target=target, text=text)
        try:
            bak_json = json.loads(response_text)
            return_text = bak_json[0][0][0]
            return_text = cls.deal_punctuation(return_text)
            return True, return_text
        except Exception as e:
            return False, ""

    @classmethod
    def ja2cn(cls, text: str) -> typing.Tuple[bool, str]:
        """
        日文->中文
        :param text: 需要翻译的文本
        :return: tuple(bool:是否翻译成功 str:翻译结果)
        """
        source = "ja"
        target = "zh-CN"
        response_text = cls.__send_requests(source=source, target=target, text=text)
        try:
            bak_json = json.loads(response_text)
            return_text = bak_json[0][0][0]
            return_text = cls.deal_punctuation(return_text)
            return True, return_text
        except Exception as e:
            return False, ""


def trans(infoproc:str,mode:int):
    fun={1:GoogleTranslate.en2cn,2:GoogleTranslate.cn2en,
         3:GoogleTranslate.ja2en,4:GoogleTranslate.ja2cn}
    return fun[mode](infoproc)


