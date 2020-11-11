from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here
import ast

class ListField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class gep(models.Model):
    id = models.IntegerField(verbose_name="编号",primary_key=True)
    file_name = models.CharField(max_length=100,verbose_name="文件名", default="")
    col_name = models.CharField(max_length=50,verbose_name="列名", default="")
    desc = models.CharField(max_length=1200,verbose_name="详细信息",default="")
    vec = ListField()

    #
    # class Meta:
    #     verbose_name = '视频名称'
    #     verbose_name_plural = verbose_name

    def __str__(self):
        return self.file_name+'----'+self.col_name
#
# class souci(models.Model):
#     titstr = models.CharField(max_length=200,verbose_name="搜索关键词")
#
#     def __str__(self):
#         return self.titstr