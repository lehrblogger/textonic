from textonic_webui.mt_batches.models import AWSUser, Instruction, Tag, Task, OrigMessage, InstructionForm, InstructionFormAll, TagForm
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
			generator = HITGenerator(AWS_KEY = AWSUser.objects.get(pk=2).aws_key, 
									 AWS_SECRET = AWSUser.objects.get(pk=2).aws_secret,
									 question_list = [[str(m.message),str(m.id)] for m in OrigMessage.objects.all()],
									 answer_options = [[str(t.tag),str(t.id)] for t in i.available_tags.all()], 
									 title = i.instruction_title,
									 description = i.instruction_text, 
									 keywords = ['data_classification', 'reading'],
									 answer_style = str(i.get_answer_style()),
        							 annotation = str(i.id), 
        							 reward = i.task_reward,
        							 assignment_count = i.max_workers_per_message)
#         	debug_list = [generator.AWS_KEY, 
#         				  generator.AWS_SECRET,
#         				  generator.question_list, 
#         				  generator.answer_options, 
#         				  generator.title, 
#         				  generator.description, 
#         				  generator.keywords, 
#         				  generator.answer_style, 
#         				  generator.annotation, 
#         				  generator.reward, 
#         				  generator.assignment_count]
#       		return render_to_response("mt_batches/text.html", {"text_list": debug_list, 'extra': dir(debug_list)})
			
        	ret_val = generator.SubmitHIT(sandbox = 'true')
        	t = Task(hit_id=ret_val)
        	t.save()
        	#return render_to_response("mt_batches/text.html", {"text_list": '', 'extra': ret_val})
        	i.submitted_tasks.add(t)
        	f.save()
        	return HttpResponseRedirect("/mt_batches/instructions")
	else:
		f = InstructionFormAll(instance=i)
		
	return render_to_response("mt_batches/instruction_info.html", {"form": f})
	
