CXX = g++
CXXFLAGS = -pthread -O3 -march=native

CPPS = $(wildcard *.cpp)
OUTS = $(patsubst %.cpp,%.out,$(CPPS))

.PHONY: all clean run

all: $(OUTS)

%.out : %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -rf $(OUTS)

################################################################################

TARGET ?= FB15K
iPath  =  ./benchmarks/$(TARGET)/
oPath  =  ../data/$(TARGET)/

SIZE   = 10
EPOCHS = 10

run: $(oPath)entity2vec.unif $(oPath)relation2vec.unif | $(oPath)
	./db.py $(iPath) $(oPath)
	./task.py $(oPath)

$(oPath)entity2vec.unif $(oPath)relation2vec.unif: | $(oPath)
	./transE.out -thread 32 -input $(iPath) -output $(oPath) -size $(SIZE) -sizeR $(SIZE) -epochs $(EPOCHS)

$(oPath):
	@ mkdir -p $@
