from django.conf.urls.defaults import *
from textonic_webui.mt_batches.models import Instruction, Tag

instruction_dict = {
    'queryset': Instruction.objects.all(),
}
tag_dict = {
    'queryset': Tag.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', instruction_dict),
    (r'^instructions/$', 'django.views.generic.list_detail.object_list', instruction_dict),
    (r'^tags/$', 'django.views.generic.list_detail.object_list', tag_dict),
    (r'^create_instruction/$', 'textonic_webui.mt_batches.views.create_instruction'),
    (r'^create_tag/$', 'textonic_webui.mt_batches.views.create_tag'),
#  (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
# url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/results.html'), 'poll_results'),
#(r'^(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),    
)
