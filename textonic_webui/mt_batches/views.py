from textonic_webui.mt_batches.models import AWSUser, Instruction, Tag, OrigMessage, InstructionForm, InstructionFormAll, TagForm
from textonic_webui.backend.textonic import HITGenerator
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect

from django.core.urlresolvers import reverse



def create_tag(request):
    t = Tag()
    if request.method == 'POST':
        f = TagForm(request.POST, instance=t)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect("/mt_batches/tags")
    else:
        f = TagForm(instance=t)
        
    return render_to_response("mt_batches/tag_new.html", {"form": f})


def submit_HIT(request):
    #submit code here    
    return HttpResponseRedirect("/mt_batches/instructions")



def create_instruction(request):
    i = Instruction()
    if request.method == 'POST':
        f = InstructionForm(request.POST, instance=i)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect("/mt_batches/instructions")
    else:
        f = InstructionForm(instance=i)
        
    return render_to_response("mt_batches/instruction_new.html", {"form": f})


def instruction_info(request, object_id):
	i = get_object_or_404(Instruction, pk=object_id)
	if request.method == 'POST':
		f = InstructionFormAll(request.POST, instance=i)
			
		if f.is_valid():
			generator = HITGenerator(AWS_KEY = '124AK6CEGM0WVXGYT202',#AWSUser.objects.get(pk=1).aws_key, 
									 AWS_SECRET = 'X5UpQYZKU8s9KtZ6qn7FSABlIgxg14yOyuCjgI+1', #AWSUser.objects.get(pk=1).aws_secret,
									 question_list = [[m.message, m.id] for m in OrigMessage.objects.all()],
									 answer_options = [[t.tag, t.id] for t in i.available_tags.all()], 
									 title = i.instruction_title,
									 description = i.instruction_text, 
									 keywords = ['data classification', 'reading'],
									 answer_style = i.get_answer_style(),
        							 annotation = i.id, 
        							 reward = i.task_reward,
        							 assignment_count = i.max_workers_per_message)
        	ret_val = generator.SubmitHIT(sandbox = 'true')
        	i.submitted_tasks.add(Task(hit_id=ret_val))
        	f.save()
        	return HttpResponseRedirect("/mt_batches/instructions")
	else:
		f = InstructionFormAll(instance=i)
		
	return render_to_response("mt_batches/instruction_info.html", {"form": f})
	
