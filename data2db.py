import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project1.settings")
import numpy as np
import django
django.setup()
from gep_search.models import gep
def main():
    dataset = np.load('./dataset.npy')
    sample_cond = np.load('./sample_cond.npy')
    datalist = []
    # dataset = dataset[:10]
    for i in range(len(dataset)):
        fn = sample_cond[i].split('---')[0]
        cn = sample_cond[i].split('---')[1]

        data_obj = gep(id = i, file_name=fn, col_name=cn, vec=list(dataset[i]))
        datalist.append(data_obj)
        if i %500 == 0:
            gep.objects.bulk_create(datalist)
            datalist = []
    gep.objects.bulk_create(datalist)

if __name__ == "__main__":
    main()
