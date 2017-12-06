# -*- coding: utf-8 -*-

from ..internal.OCR import OCR


class VerticalShift(OCR):
    __name__ = "VerticalShift"
    __type__ = "ocr"
    __version__ = "0.01"
    __status__ = "testing"

    __description__ = """ocr plugin for captchas where all letters are just vertically shifted"""
    __license__ = "GPLv3"
    __authors__ = [("igel", None)]

    def recognize(self, image):
        self.load_image(image)
        self.to_greyscale()
        self.eval_black_white(20)
        self.img = self.join_letters(self.split_captcha_letters())
        self.run_tesser(pagesegmode=7)
        return self.result_captcha
