from django.conf.urls.defaults import *
from textonic_webui.mt_batches.models import Instruction

info_dict = {
    'queryset': Instruction.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'textonic_webui.mt_batches.views.create_tags'),
    (r'^instructions/$', 'textonic_webui.mt_batches.views.create_instructions'),
    (r'^tags/$', 'textonic_webui.mt_batches.views.create_tags'),
)
