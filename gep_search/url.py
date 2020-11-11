from django.conf.urls import url
from django.urls import re_path
from django.views.generic import RedirectView
from gep_search.views import *



urlpatterns = [
    url(r'^$',index,name="index"),
    url(r'^guide$',tages,name="tages"),
    url(r'^result', upload_file,name="result_page"),
    # url(r'^sct', scatter_close,name="scatter_close"),
    url(r'^scatter', scatter,name="scatter"),
    re_path(r'^download',DownLoadApiView , name="download"),
    re_path(r'^2download',DownLoadApiView2, name="download2"),
    # url(r'^favicon.ico', RedirectView.as_view(url=r'/static/img/favicon.ico'))
]