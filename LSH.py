import heapq
import json
import struct
import pickle
import redis
import numpy as np
import math
import time
import json
import os
# import django
# django.setup()
# from gep_search.models import gep
from django_redis import get_redis_connection
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from django.core.cache import cache

def read_data(mode):
    if mode == 'a':
        dataset = np.load('./dataset.npy')
        sample_cond = np.load('./sample_cond.npy',allow_pickle=True)
        data_num = len(dataset)
        dim = len(dataset[0])
        tables = np.load('./tables.npy', allow_pickle=True)
        planes = np.load('./planes.npy')


        return dataset,data_num, dim, sample_cond, tables, planes
    else:
        sample_cond = np.load('./sample_cond.npy',allow_pickle=True)
        dim = 44111
        tables = np.load('./tables.npy', allow_pickle=True)
        planes = np.load('./planes.npy')
        return dim, sample_cond, tables, planes



def length(v):
    """returns the length of a vector"""
    return math.sqrt(np.dot(v, v))

def l2(v1,v2):
    # assert len(v1) == len(v2)
    v1 =np.array(v1)
    v2 =np.array(v2)
    return np.sum((v1-v2)**2)**0.5

def cos_sim(v1, v2):
    return l2(v1, v2)
    assert len(v1) == len(v2)
    v1 = v1.astype('float32')
    # v2 = v2.astype('float32')
    return np.dot(v1,v2)/ length(v1)/length(v2)

def linear_search(data, q, k):

    max_cos= cos_sim(data[0], q)
    res = 0
    data_num = len(data)
    topk_sim = [(np.inf, 0) for i in range(k)]
    heapq.heapify(topk_sim)
    for p in range(data_num):
        cosine = cos_sim(data[p], q)
        if cosine < topk_sim[0][0] and np.sum([p == i[1] for i in topk_sim]) == 0:
            # print('before: ',topk_sim)
            heapq.heappop(topk_sim)
            heapq.heappush(topk_sim, (cosine, p))
        if cosine > max_cos:
            max_cos = cosine
            res = p
        # print('cos = ',cosine)
    return  topk_sim

def d2rank(data):
    data = data.reshape(1,-1)
    for d in data:
        n0s = np.sum(d<=0)
        d2r = np.argsort(d)

        d[d2r] = range(38313)
        d -= n0s
        d[d<0] = 0
    return data

def standardrized(d):
    mu = np.mean(d)
    sigmoid = np.std(d)

    return (d-mu)/sigmoid

def test2(file_name, up2db, sample_condition, topk, ip):
    # dim, sample_cond ,tables, planes= read_data('b')

    # # print(tables)
    # print(len(planes))
    s1 = time.clock()
    conn = get_redis_connection('default')

    jgn2ind,pq, jsam, dataset= conn.mget(['gn2ind','pq','sample_cond','dataset'])
    e3 = time.clock()
    gn2ind = json.loads(jgn2ind)
    pq = pickle.loads(pq)
    sample_cond = json.loads(jsam)



    h, w = struct.unpack('>II', dataset[:8])
    dataset = np.frombuffer(dataset, dtype=np.uint8, offset=8).reshape(h, w)
    print('load data time:',e3-s1)
    # print('dnum = ',dnum)
    # assert 1==0
    dnum = dataset.shape[0]
    print('shape = ',dataset.shape)
    query_q = np.zeros(38313, dtype='float32')
    format_error = False
    count_line = 0
    q_sample = ''
    q_cond=''
    with open(file_name) as f:

        for line in f:
            count_line+=1

            cont = line.split('\t')
            if count_line ==1:
                q_cond = cont[1]
            if len(cont) < 2 :
                format_error = True
                break
            gn = cont[0].strip()
            # assert 1==0
            q_sample += '\t'.join(cont[:2])+'\n'
            if gn in gn2ind:
                try:
                    query_q[gn2ind[gn]] = float(cont[1])
                except:
                    format_error = True
                    break
    if format_error or count_line<100:
        print(count_line)
        return 'format error',0




    #----------rank_stand
    query_q = d2rank(query_q)
    query_q = standardrized(query_q)[0]

    # query_q = pq.encode(query_q.reshape((1,-1)))
    k = topk

    dists = pq.dtable(query=query_q).adist(codes=dataset)

    top_n = np.argsort(dists)
    topk_sim = top_n[:k]

    e4 = time.clock()
    print('linear:', e4 -s1)
    sims = []
    conditions = []
    # print('sum = ',np.sum(dists), dnum)

    if up2db:
        q_coded = pq.encode(query_q.reshape(1,-1))
        print('before',dataset.shape)
        dataset = np.insert(dataset,dnum,values=q_coded,axis=0)
        print(dataset.shape, sample_condition)
        sample_cond.append(sample_condition)
        # dsam = json.dumps(sample_cond)



    jdata = json.loads(conn.get('data_desc'))
    for i in topk_sim:
        (l2, ind) = (dists[i], i)
        sim = 1- l2/38313/2
        sims.append(sim)
        conditions.append(sample_cond[ind])
        jdata[i]['similar'] = 'yes'
        jdata[i]['spearman'] = str(sim)
    print(ip)
    # json_file = 'data'+ip+'.json'
    # with open('./gep_search/static/'+json_file, 'w') as f:
    #     json.dump(jdata,f)
    cache.set('data_desc'+ip, json.dumps(jdata), timeout=1800)
    print(topk_sim)

    # sims = sims[::-1]
    # conditions = conditions[::-1]
    # print(topk_data.shape)


    return conditions, sims

