from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

data = np.load('./data_rank_and_norm_float16.npy')

data = data.reshape(2788,-1)
print(data.shape)
query = data[732]


top_30 = [ 732 ,733,  734,  393 , 392,  744, 1608, 1609,  867,
           871,1603,1602,982,981,969,980,970,968,1607,1610,1612,1611,1604,1606,678,1615,681,679,680,676]
# i = 0
# new_data = np.zeros((data.shape))
# for d in new_data:
#     d[data[i]==query]=1
#     i+=1
# print(new_data.shape)

# pca= PCA(n_components=3)
# data_pca = pca.fit_transform(data[:1000])

# fig, ax = plt.subplots()
# for i in range(int(data_pca.size / 2)):
#     team = data_pca[i]
#     if i in top_30:
#         ax.scatter(team[0], team[1], c='r',s=1)
#     else:
#         ax.scatter(team[0], team[1], c='b', s=1)

    # ax.annotate(team_name[i], (team[0], team[1]))
# plt.show()

# from mpl_toolkits.mplot3d import Axes3D
#
# fig, ax = plt.subplots()
# ax = Axes3D(fig)
# for i in range(int(data_pca.size / 3)):
#     team = data_pca[i]
#     if i in top_30:
#         ax.scatter(team[0], team[1], team[2],c='r',s=1)
#     else:
#         ax.scatter(team[0], team[1], team[2],c='b', s=1)
    # ax.legend()
    # ax.text(team[0], team[1], team[2],team_name[i])
# plt.show()

tsne = TSNE(n_components=2,init='pca')


data_tsne = tsne.fit_transform(data[:])
data_2d = []
fig, ax = plt.subplots()
for i in range(int(data_tsne.size / 2)):
    team = data_tsne[i]
    data_2d.append(team)
    if i in top_30:
        ax.scatter(team[0], team[1],c='r',s=1)
        if i == 732:
            ax.scatter(team[0], team[1],c='green',s=1)
    else:
        ax.scatter(team[0], team[1], c='b', s=1)

# np.save('./dataset_2d', np.array(data_2d))

# fig = plt.figure()
# ax = Axes3D(fig)
#
# for i in range(int(data_tsne.size / 3)):
#     team = data_tsne[i]
#     if i in top_30:
#         ax.scatter3D(team[0], team[1], team[2], c='r',s=1)
#         if i == 732:
#             ax.scatter(team[0], team[1], team[2], c='green', s=1)
#     else:
#         ax.scatter3D(team[0], team[1], team[2], c='b',s =1)
#
# plt.show()



# plt.savefig('./3d.jpg', dpi=300,bbox_inches='tight')

