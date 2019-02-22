#!/bin/sh -x

relation=$1
dataPath=../data/FB15K/
taskPath=${dataPath}tasks/${relation}/


SIZE=10
EPOCHS=10

../tool/transE.out -thread 32 -input ${taskPath} -output ${taskPath} -size ${SIZE} -sizeR ${SIZE} -epochs ${EPOCHS}
../tool/transH.out -thread 32 -input ${taskPath} -output ${taskPath} -size ${SIZE} -sizeR ${SIZE} -epochs ${EPOCHS}
../tool/transR.out -thread 32 -input ${taskPath} -output ${taskPath} -size ${SIZE} -sizeR ${SIZE} -epochs ${EPOCHS}
../tool/transD.out -thread 32 -input ${taskPath} -output ${taskPath} -size ${SIZE} -sizeR ${SIZE} -epochs ${EPOCHS}

wait

ls ${taskPath}
