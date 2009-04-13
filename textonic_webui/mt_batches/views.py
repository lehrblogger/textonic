from textonic_webui.mt_batches.models import Instruction, Tag
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse 


def create_instructions(request):
    InstructionFormSet = modelformset_factory(Instruction)
    if request.method == 'POST':
        formset = InstructionFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = InstructionFormSet()
    return render_to_response("mt_batches/instruction_detail.html", {
        "formset": formset,
    })

def create_tags(request):
    TagFormSet = modelformset_factory(Tag)
    if request.method == 'POST':
        formset = TagFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = TagFormSet()
    return render_to_response("mt_batches/tag_detail.html", {
        "formset": formset,
    })
