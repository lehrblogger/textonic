from textonic_webui.mt_batches.models import Instruction, Tag, InstructionForm, InstructionFormAll, TagForm
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
            request.user.message_set.create(message='Please check your data.')
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
            request.user.message_set.create(message='Please check your data.')
    else:
        f = InstructionForm(instance=i)
        
    return render_to_response("mt_batches/instruction_new.html", {"form": f})


def instruction_info(request, object_id):
	i = get_object_or_404(Instruction, pk=object_id)
	if request.method == 'POST':
		f = InstructionFormAll(request.POST, instance=i)
		f.TextInput(attrs={'disabled': 'disabled'})

		if f.is_valid():
			f.save()
			#submit here
		else:
			request.user.message_set.create(message='Please check your data.')
	else:
		f = InstructionFormAll(instance=i)
    
	return render_to_response("mt_batches/instruction_info.html", {"form": f})
	
