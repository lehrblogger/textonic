from textonic import HITGenerator, HITRetriever

AWS_ACCESS_KEY_ID = '124AK6CEGM0WVXGYT202'
AWS_SECRET_ACCESS_KEY = 'X5UpQYZKU8s9KtZ6qn7FSABlIgxg14yOyuCjgI+1'

#TEST_HIT_ID = 'M2Q8WKYTXK4Z5M967WA0' # Good test submission
#TEST_HIT_ID = 'AXPZ7TYA5WP03N8XN1C0' # HIT SUBMISSION 1
#TEST_HIT_ID = 'MJNZG5ZFK03ZJ08R2W70' # HIT SUBMISSION 2
#TEST_HIT_ID = '3AQTVBZDWA2PW44ZKW50' # HIT SUBMISSION 3
#TEST_HIT_ID = 'RHQ8XFY4V32Z6W8PBWYZ' # HIT SUBMISSION 4 - 10 ASSIGNMENTS

TEST_HIT_ID = 'RHQ8XFY4V32Z6W8PBWYZ' # HIT SUBMISSION 4 - 10 ASSIGNMENTS
test_retriever = HITRetriever(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TEST_HIT_ID)
print test_retriever.RetrieveHIT()
