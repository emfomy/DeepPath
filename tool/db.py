#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2019'

import os
import sys

def main():

    assert len(sys.argv) == 3

    iPath = sys.argv[1]
    oPath = sys.argv[2]

    # Entity ID
    id2entity = []
    with open(os.path.join(iPath, 'entity2id.txt'), 'r') as fin:
        print('<< '+fin.name)
        next(fin)
        for line in fin:
            name, idx = line.strip().split()
            idx = int(idx)
            assert idx == len(id2entity)
            id2entity.append('E!'+name)

    with open(os.path.join(oPath, 'entity2id.txt'), 'w') as fout:
        print('>> '+fout.name)
        for idx, name in enumerate(id2entity):
            print(f'{name}\t{idx}', file=fout)

    # Relation ID
    id2relation = []
    with open(os.path.join(iPath, 'relation2id.txt'), 'r') as fin:
        print('<< '+fin.name)
        next(fin)
        for line in fin:
            name, idx = line.strip().split()
            idx = int(idx)
            assert idx == len(id2relation)
            id2relation.append('R!'+name)

    with open(os.path.join(oPath, 'relation2id.txt'), 'w') as fout:
        print('>> '+fout.name)
        for idx, name in enumerate(id2relation):
            print(f'{name}\t{idx}', file=fout)
        idx0 = len(id2relation)
        for idx, name in enumerate(id2relation):
            print(f'{name}_inv\t{idx+idx0}', file=fout)

    # KB
    kb = []
    with open(os.path.join(iPath, 'test2id.txt'), 'r') as fin:
        print('<< '+fin.name)
        next(fin)
        kb += [tuple(map(int, line.strip().split())) for line in fin]

    with open(os.path.join(iPath, 'valid2id.txt'), 'r') as fin:
        print('<< '+fin.name)
        next(fin)
        kb += [tuple(map(int, line.strip().split())) for line in fin]

    with open(os.path.join(oPath, 'kb_env_rl.txt'), 'w') as fout:
        print('>> '+fout.name)
        for e1, e2, r in kb:
            print(f'{id2entity[e1]}\t{id2entity[e2]}\t{id2relation[r]}', file=fout)
            print(f'{id2entity[e2]}\t{id2entity[e1]}\t{id2relation[r]}_inv', file=fout)

    # train
    id2label = {1: '+', -1: '-'}
    with open(os.path.join(iPath, 'test_neg.txt'), 'r') as fin:
        print('<< '+fin.name)
        next(fin)
        train_tuple = [tuple(map(int, line.strip().split())) for line in fin]

    with open(os.path.join(oPath, 'train.txt'), 'w') as fout:
        print('>> '+fout.name)
        for e1, e2, r, l in train_tuple:
            print(f'{id2entity[e1]}\t{id2entity[e2]}\t{id2relation[r]}\t{id2label[l]}', file=fout)

    # test
    id2label = {1: '+', -1: '-'}
    with open(os.path.join(iPath, 'valid_neg.txt'), 'r') as fin:
        print('<< '+fin.name)
        next(fin)
        test_tuple = [tuple(map(int, line.strip().split())) for line in fin]

    with open(os.path.join(oPath, 'test.txt'), 'w') as fout:
        print('>> '+fout.name)
        for e1, e2, r, l in test_tuple:
            print(f'{id2entity[e1]}\t{id2entity[e2]}\t{id2relation[r]}\t{id2label[l]}', file=fout)


if __name__ == '__main__':
    main()
    sys.exit()
