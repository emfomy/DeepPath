#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2019'

import os
import re
import subprocess
import sys

def main():

    assert len(sys.argv) == 2

    iPath = sys.argv[1]

    # Entity ID
    with open(os.path.join(iPath, 'entity2id.txt'), 'r') as fin:
        print('<< '+fin.name)
        entity2id = {}
        id2entity = []
        for line in fin:
            name, idx = line.strip().split()
            idx = int(idx)
            assert idx == len(id2entity)
            entity2id[name] = idx
            id2entity.append(name)

    # Relation ID
    with open(os.path.join(iPath, 'relation2id.txt'), 'r') as fin:
        print('<< '+fin.name)
        relation2id = {}
        id2relation = []
        for line in fin:
            if '@' in line: break
            name, idx = line.strip().split()
            idx = int(idx)
            assert idx == len(id2relation)
            relation2id[name] = idx
            id2relation.append(name)

    # KB
    with open(os.path.join(iPath, 'kb_env_rl.txt'), 'r') as fin:
        print('<< '+fin.name)
        kb = [tuple(line.strip().split()) for line in fin]

    with open(os.path.join(iPath, 'train.txt'), 'r') as fin:
        print('<< '+fin.name)
        train_tuple = [tuple(line.strip().split()) for line in fin]

    with open(os.path.join(iPath, 'test.txt'), 'r') as fin:
        print('<< '+fin.name)
        test_tuple = [tuple(line.strip().split()) for line in fin]

    # Task
    for taskname in id2relation:
        print(taskname)
        oPath = os.path.join(iPath, 'tasks', str(re.sub(r'\W', '_', taskname)))
        os.makedirs(oPath, exist_ok=True)

        with open(os.path.join(oPath, 'name'), 'w') as fout:
            print('>> '+fout.name)
            print(taskname, file=fout)

        entities = set()
        transX   = []
        with open(os.path.join(oPath, 'graph.txt'), 'w') as fout:
            print('>> '+fout.name)
            for line in kb:
                if line[2] != taskname and line[2] != taskname+'@inv':
                    entities.add(line[0])
                    print('\t'.join((line[0], line[2], line[1],)), file=fout)
                    if '@' not in line[2]: transX.append(line)

        with open(os.path.join(oPath, 'train_pos'), 'w') as fout:
            print('>> '+fout.name)
            count = 0
            for line in kb:
                if count > 10: break
                if line[2] == taskname and line[0] in entities:
                    transX.append(line)
                    count += 1
                    print('\t'.join(line), file=fout)

        # ID
        with open(os.path.join(oPath, 'entity2id.txt'), 'w') as fout:
            print('>> '+fout.name)
            print(len(id2entity), file=fout)
            for idx, name in enumerate(id2entity):
                print(f'{name}\t{idx}', file=fout)

        with open(os.path.join(oPath, 'relation2id.txt'), 'w') as fout:
            print('>> '+fout.name)
            print(len(id2relation), file=fout)
            for idx, name in enumerate(id2relation):
                print(f'{name}\t{idx}', file=fout)

        with open(os.path.join(oPath, 'train2id.txt'), 'w') as fout:
            print('>> '+fout.name)
            print(len(transX), file=fout)
            for line in transX:
                print(f'{entity2id[line[0]]}\t{entity2id[line[1]]}\t{relation2id[line[2]]}', file=fout)

        # Train
        with open(os.path.join(oPath, 'train.pairs'), 'w') as fout:
            print('>> '+fout.name)
            count = 0
            for line in train_tuple:
                if count > 20: break
                if line[2] == taskname:
                    count += 1
                    print(f'thing${line[0]},thing${line[1]}:{line[3]}', file=fout)

        # Test
        with open(os.path.join(oPath, 'test.pairs'), 'w') as fout:
            print('>> '+fout.name)
            count = 0
            for line in test_tuple:
                if count > 20: break
                if line[2] == taskname:
                    count += 1
                    print(f'thing${line[0]},thing${line[1]}:{line[3]}', file=fout)

        print('>> '+os.path.join(oPath, 'sort_test.pairs'))
        subprocess.run(['sort', os.path.join(oPath, 'test.pairs'), '-o', os.path.join(oPath, 'sort_test.pairs')])

        break


if __name__ == '__main__':
    main()
    sys.exit()
