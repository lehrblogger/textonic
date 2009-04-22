from textonic import HITGenerator

AWS_ACCESS_KEY_ID = '124AK6CEGM0WVXGYT202'
AWS_SECRET_ACCESS_KEY = 'X5UpQYZKU8s9KtZ6qn7FSABlIgxg14yOyuCjgI+1'

questions = [['Select yes','I said select yes'],['Select no','I said select no'],['Select maybe','I said select maybe']]
style = 'radiobutton'
options = [['Yes','yes'],['No','no'],['Maybe','maybe']]
title = 'Simple test'
description = 'A simple test of the textonic HIT submission system'
keywords = ['textonic','boto','test']

test_generator = HITGenerator(AWS_KEY = AWS_ACCESS_KEY_ID,
				AWS_SECRET = AWS_SECRET_ACCESS_KEY,
				question_list = questions,
				answer_style = style,
				answer_options = options,
				title = title,
				description = description,
				keywords = keywords,
				reward = 0.05,
				assignment_count = 10)
print test_generator.SubmitHIT(sandbox='true')
