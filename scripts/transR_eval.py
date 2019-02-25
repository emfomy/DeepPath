import pickle
import sys
import numpy as np

from cfg import DATAPATH as dataPath
from util import *

relation = sys.argv[1]

dataPath_ = dataPath + 'tasks/' + relation
ent_id_path = dataPath + 'entity2id.txt'
rel_id_path = dataPath + 'relation2id.txt'
test_data_path = dataPath + 'tasks/' + relation + '/sort_test.pairs'

from utils import embedding_dim0

f1 = open(ent_id_path)
f2 = open(rel_id_path)
content1 = f1.readlines()
content2 = f2.readlines()
f1.close()
f2.close()

entity2id = {}
relation2id = {}
for line in content1:
	entity2id[line.split()[0]] = int(line.split()[1])

for line in content2:
	relation2id[line.split()[0]] = int(line.split()[1])


ent_vec = np.loadtxt(dataPath_ + '/entity2vec.bern')
rel_vec = np.loadtxt(dataPath_ + '/relation2vec.bern')
M = np.loadtxt(dataPath_ + '/A.bern')
M = M.reshape([-1,embedding_dim0,embedding_dim0])

f = open(test_data_path)
test_data = f.readlines()
f.close()

test_pairs = []
test_labels = []
# queries = set()
for line in test_data:
	e1 = line.split(',')[0].replace('thing$','')
	#e1 = '/' + e1[0] + '/' + e1[2:]
	e2 = line.split(',')[1].split(':')[0].replace('thing$','')
	#e2 = '/' + e2[0] + '/' + e2[2:]
	test_pairs.append((e1,e2))
	label = 1 if line[-2] == '+' else 0
	test_labels.append(label)


aps = []
query = test_pairs[0][0]
y_true = []
y_score = []

score_all = []

rel = relation.replace("_", ":")
relation_vec = np.expand_dims(rel_vec[relation2id[rel],:],0)
M_vec = M[relation2id[rel],:,:]

for idx, sample in enumerate(test_pairs):
	#print_status('query node: ', sample[0], idx)
	if sample[0] == query:
		e1_vec = np.expand_dims(ent_vec[entity2id[sample[0]],:],0)
		e2_vec = np.expand_dims(ent_vec[entity2id[sample[1]],:],0)

		e1_vec_rel = np.matmul(e1_vec, M_vec)
		e2_vec_rel = np.matmul(e2_vec, M_vec)
		score = -np.sum(np.square(e1_vec_rel + relation_vec - e2_vec_rel))

		score_all.append(score)
		y_score.append(score)
		y_true.append(test_labels[idx])
	else:
		query = sample[0]
		count = list(zip(y_score, y_true))
		count.sort(key = lambda x:x[0], reverse=True)
		#print_status(count)
		ranks = []
		correct = 0
		for idx_, item in enumerate(count):
			if item[1] == 1:
				correct +=  1
				ranks.append(correct/(1.0+idx_))
		if len(ranks)==0:
			ranks.append(0)
		aps.append(np.mean(ranks))
		# if len(aps) % 10 == 0:
			# print_status('How many queries:', len(aps))
			# print_status(np.mean(aps))
		y_true = []
		y_score = []

		e1_vec = np.expand_dims(ent_vec[entity2id[sample[0]],:],0)
		e2_vec = np.expand_dims(ent_vec[entity2id[sample[1]],:],0)
		e1_vec_rel = np.matmul(e1_vec, M_vec)
		e2_vec_rel = np.matmul(e2_vec, M_vec)
		score = -np.sum(np.square(e1_vec_rel + relation_vec - e2_vec_rel))
		score_all.append(score)
		y_score.append(score)
		y_true.append(test_labels[idx])


score_label = zip(score_all, test_labels)
score_label_ranked = sorted(score_label, key = lambda x:x[0], reverse=True)

mean_ap = np.mean(aps)
print_status('TransR MAP: ', mean_ap)


