# import struct
# import numpy as np
from django.http import HttpResponse,HttpRequest
from django.shortcuts import render, redirect
# from django.conf import settings
# from django.core.paginator import Paginator ,InvalidPage,EmptyPage,PageNotAnInteger #导入paginator实现分页功能，并且引入他的3个异常类型
# from flask import jsonify
# from django.template import RequestContext
import os
from django.views.decorators.csrf import csrf_exempt
import LSH
from django_redis import get_redis_connection
# from numpy import frombuffer,float16
from django.core.cache import cache


# from gep_search.models import *
import json
# Create your views here.

def index(request):
    # conn = get_redis_connection('default')
    # encoded = conn.get(0)
    # h, w = struct.unpack('>II', encoded[:8])
    # a = frombuffer(encoded, dtype=float16, offset=8).reshape(h, w)[0]
    # print(a[:10])
    return render(request,'index.html')    #   loacals():把方法中的变量传给模板

def tages(request):
    return render(request,'guide.html',locals())

@csrf_exempt
def upload_file(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    if request.method == "POST":
        up_content = {}
        msg = []
        res_list = []
        myFile = request.FILES.get("query", None)  # 获取上传的文件，如果没有文件，则默认为None
        sample_cd = request.POST.get('sample_cond')
        topk = request.POST.get('topk')
        if topk == '':
            topk = 10
        else:
            topk = int(topk)
        up2db = request.POST.get('check2')
        if up2db:
            if len(sample_cd)>0:
                pass
            else:
                msg.append("上传到数据库必须输入样本信息")
                return render(request, 'index.html', {'message': msg})
        print('my:=======', myFile)
        print('sample_cond = ',sample_cd)

        if not myFile:
            msg.append("upload failed")
            return render(request, 'index.html', {'message': msg})
        myFilename = str(myFile)
        file_format = os.path.splitext(myFilename)[1]
        # print(file_format, file_format != 'txt')
        if file_format != '.txt' and file_format != '.tsv':
            msg.append("upload failed, only accepts in .txt and .tsv format")
            return render(request, 'index.html', {'reslist': res_list, 'message': msg})
        upload_path = './upload/'
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)
        destination = open(upload_path + myFile.name, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        # up_content['flag'] = True
        fast = False
        res, sim = LSH.test2(upload_path + myFile.name, up2db,sample_cd, topk,ip)
        gep_id = ''
        if res == 'format error':
            msg.append("format error")
            os.remove(upload_path + myFile.name)
            return render(request, 'index.html', {'message': msg})
        else:
            con = get_redis_connection('default')
            sam_detail = con.get('sam_detail')
            sam_detail = json.loads(sam_detail)
            for i in range(len(res)):

                # res[i] = res[i].replace('---','+++')
                sim[i] = round(sim[i], 4)
                # file_name = res[i].split('---')[0]
                # file_name = file_name.replace('-',' ')

                # print(gep_id+column_n)
                if res[i] not in sam_detail:
                    pass
                else:
                    #gsm, tissue, genotype, growth, characs = sam_detail[gep_id+column_n]
                    gsm, title, characs = sam_detail[res[i]]
                   # if len(tissue)==0 or tissue[0].upper() == 'WT':
                   #     tissue=['Unknown']
                   # if len(genotype) ==0:
                   #     genotype=['Unknown']
                   # if len(growth) == 0:
                   #     growth = ['Unknown']
                    if len(characs) == 0:
                        characs = ['Unknown']
                    if len(title) == 0:
                        title = ['Unknown']
                    characs = characs[0].split('<br>')

                    # print(characs)
                    res_list.append([gsm, title[0],characs, sim[i], gep_id])
        return render(request, 'result_page.html', {'reslist': res_list, 'message': msg, 'gep_id': gep_id})
    return redirect('/')

def DownLoadApiView2(request):
    """
        API文档下载
    :param request:
    :return:
    """

    if request.method == "GET":
        file = open('gep_search/templates/query_sample.txt', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="query_sample.txt"'
        return response

def DownLoadApiView(request):
    """
        API文档下载
    :param request:
    :return:
    """
    # print(request.GET.get('href'))
    if request.method == "GET":
        file = open('gep_search/templates/gene_result.txt', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="gene_names.txt"'
        return response

def scatter(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    print(cache.ttl('data_desc'+ip))
    if cache.ttl('data_desc'+ip) == 0:
        return render(request,'index.html')
    else:
        dataj = json.loads(cache.get('data_desc'+ip))
        return render(request,'index0.html', locals())
