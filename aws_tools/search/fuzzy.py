# -*- coding: utf-8 -*-

from fuzzywuzzy import process

choices = ["aws_data_lab_sanhe", "aws sandbox", "sanhe dev user"]
s = process.extract("aws sanhe", choices, limit=2)
print(s)