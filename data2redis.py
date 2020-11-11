
import struct

import redis
import numpy as np
import json


def add():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    con = redis.Redis(connection_pool=pool)
    print(con)

    with open('./data.json', 'r') as f:
        jdata = json.load(f)
    jdata = json.dumps(jdata)
    con.set('data_desc', jdata)

    sam_detail = np.load('./sam_details_dels2.npy', allow_pickle=True)
    sam_detail = sam_detail.item()
    con.set('sam_detail',json.dumps(sam_detail))
    sample_cond = np.load('./sample_cond_dels2.npy')

    sample_cond = list(sample_cond)
    jsam = json.dumps(sample_cond)
    gn2ind = np.load('./gn2ind.npy', allow_pickle=True)
    gn2ind = gn2ind.item()
    jgn = json.dumps(gn2ind)

    con.mset({'gn2ind': jgn, 'sample_cond': jsam})
    with open("./pq.pkl", 'rb') as file:
        pq = file.read()
    con.mset({'pq': pq})
    dataset = np.load('./dataset_pq.npy')
    datanum = dataset.shape[0]
    dataset = dataset.reshape(datanum,-1)
    print(dataset.shape)
    h, w = dataset.shape

    shape = struct.pack('>II', h, w)
    encoded = shape + dataset.tobytes()
    con.set('dataset',encoded)


def delete():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    con = redis.Redis(connection_pool=pool)

    for i in range(2788):
        con.delete(i)
    # for key in ['gn2ind','sample_cond', 'avg_val']:
    #     con.delete(key)
    # for key in ['tables', 'planes']:
    #     con.delete(key)
if __name__ == "__main__":
    add()
