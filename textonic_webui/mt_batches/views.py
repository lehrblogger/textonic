from textonic_webui.mt_batches.models import Instruction, Tag, InstructionForm, TagForm
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect


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
        
    return render_to_response("mt_batches/instruction_detail.html", {"form": f})

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
        
    return render_to_response("mt_batches/tag_detail.html", {"form": f})
