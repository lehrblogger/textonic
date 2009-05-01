# Thomas Robertson 2009
# This work should be considered part of the public domain.

import uuid
import datetime
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import Question, QuestionContent, AnswerSpecification, QuestionForm, SelectionAnswer


class HITGenerator(object):
    """
    HITGenerator contains the methods necessary to generate and register a Textonic hit.

    A Textonic hit is relatively restrictive as all questions must have precisely the same answer specification.  This means
    that HITGenerator is not as flexible as it could be, but it also means that it is a relatively simple class to use.
    """

    def __init__(self, AWS_KEY, AWS_SECRET, question_list, answer_options, title, description, keywords, answer_style = 'radiobutton',
        annotation = 'Annotation', reward = 0.50, lifetime = 60*60*24, assignment_count = 10, duration = 60*60,
        approval_delay = 60*60*12):

            # Connection attributes
        self.AWS_KEY = AWS_KEY # This is the AWS ID key for the user
        self.AWS_SECRET = AWS_SECRET # This is the AWS Secret key for the user
        self.host = 'mechanicalturk.amazonaws.com'

        self.HITId = 'NOT SUBMITTED YET'
        
            # Quesion and answer formats
        self.question_list = question_list # A list of strings containing the text of the questions this HIT will be built from
        self.answer_style = answer_style # A string determining the type of answer, for Textonic HITs this must either be 'radiobutton'
            # or 'checkbox'
        self.answer_options = answer_options # A list of pairs of strings with the first value being the answer displayed in the HIT
            # and the second value being the internal classification string

            # HIT settings
        self.title = title # A string containing the title, this should be the same for all HITs generated from a given set of
            # instructions
        self.annotation = annotation # An annotation string, used to describe a HIT internally, not publicly exposed, defaults to empty
        self.description = description # A string describing the HIT, also the same for all HITs generated from a given set
            # of instructions
        self.keywords = keywords # A list of strings to help categorize the HIT, think del.icio.us tags: descriptive with no spaces
        self.reward = reward # A floating point number of the dollar amount of the reward for completing this HIT
        self.lifetime = lifetime # Lifetime of the HIT in seconds, defaults to 24 hours
        self.assignment_count = assignment_count # The number of different people to have complete the HIT, defalts to 10
        self.duration = duration # The amount of time in seconds a user has to complete the HIT from the time they start, defaults to
            # 1 hour
        self.approval_delay = approval_delay # The amount of time in seconds before the system automatically approves payment on a
            # completed HIT
        self.hit_response = None;

    def SubmitHIT(self, sandbox = 'false'):
        """"
        Constructs a HIT from the HITGenerator's attributes, registers it with Amazon, and returns the HITId as a unicode string.

        If the sandbox flag is set to true then the hit will be registered with the Sandbox, otherwise it is registered to AWS
        directly.  All of the necessary data must have been submitted during the HITGenerator's initiation.
        """

        if sandbox is 'true':
            self.host = 'mechanicalturk.sandbox.amazonaws.com'

        conn = MTurkConnection(host = self.host, aws_access_key_id = self.AWS_KEY, aws_secret_access_key = self.AWS_SECRET)

        answer_specification = AnswerSpecification(SelectionAnswer(style = self.answer_style, selections = self.answer_options))

        questions = []
        for i in self.question_list:
	    questions.append(Question(identifier=i[1], content = QuestionContent(i[0]), answer_spec = answer_specification))

        question_form = QuestionForm(questions)

        self.hit_response = conn.create_hit(question = question_form,
                                 lifetime = self.lifetime,
                                 max_assignments = self.assignment_count,
                                 title = self.title,
                                 description = self.description,
                                 keywords = self.keywords,
                                 reward = self.reward,
                                 duration = self.duration,
                                 approval_delay = self.approval_delay,
                                 annotation = self.annotation)

            # Returns the HITId as a unicode string
        self.HITId = self.hit_response.HITId
        return self.HITId

class HITRetriever(object):
    """
    The HITRetriever class is used to retrieve a HIT and handle parsing the data from the ResponseSet.

    The HITRetriever must be passed a HITId in order to retrieve the appropriate HIT.  Once a hit is retrieved its
    responses are parsed into attributes within the HITRetriever which can be accessed directly.  HITId should be
    passed as a unicode string.
    """

    def __init__(self, AWS_KEY, AWS_SECRET, hit_id):

            # Connection attributes
        self.AWS_KEY = AWS_KEY # This is the AWS ID key for the user
        self.AWS_SECRET = AWS_SECRET # This is the AWS Secret key for the user
        self.host = 'mechanicalturk.amazonaws.com'
        self.hit_id = hit_id

    def RetrieveHIT(self, sandbox = 'false'):
        """
        RetrieveHit retrieves the HIT assigned to this object and parses its data into local attributes for later retrieval.

        If the value of sandbox is 'true' then the HIT will be retrieved from the Sandbox, otherwise it will be accessed from
        the standard AWS servers.
        """

        if sandbox is 'true':
            self.host = 'mechanicalturk.sandbox.amazonaws.com'

	conn = MTurkConnection(host = self.host, aws_access_key_id = self.AWS_KEY, aws_secret_access_key = self.AWS_SECRET)
        retrieved_hit_list = conn.get_hit(hit_id = self.hit_id)
	retrieved_hit = retrieved_hit_list[0]

	assignments_list = conn.get_assignments(hit_id = self.hit_id, page_size = retrieved_hit.MaxAssignments)

	returned_data = []

	for i in assignments_list:
		this_assignment = []
		for j in i.answers[0]:
			qa_pair = [j.QuestionIdentifier, j.SelectionIdentifier]
			this_assignment.append(qa_pair)
		returned_data.append(this_assignment)
	return returned_data
