import numpy as np
def gn2i():
    gene_name = np.load('./gene_name2.npy')
    gn_dup = np.load('./gn_dup2.npy', allow_pickle=True)

    gn_dup = gn_dup.item()  # np 读取保存字典必须

    gn2ind = {}
    gene_len = len(gene_name)
    for i in range(gene_len):
        gn2ind[gene_name[i]] = i
        if gene_name[i] in gn_dup:
            for gn in gn_dup[gene_name[i]]:
                gn2ind[gn] = i
    np.save('./gn2ind',gn2ind)
if __name__ =='__main__':
    gn2i()