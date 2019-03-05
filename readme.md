**Graph Entropy Methods **
=============
This is the implementation of Graph Entropy-based Method (GEM) to detect concept drift in graph streams.
This apply a sliding window technique on the data stream and compute graph entropy for the subgraphs in the window w.r.t. their class membership.
Different from most popular drift detectors that use classification outputs (e.g., error rate) as indicators for detecting concept change,
this approach investigates the intrinsic properties of the data (i.e., subgraph distribution w.r.t. class membership).
Consequently, a series of entropy values is obtained while sliding the window on the stream by moving one instance forward at each step.
It then employ the Cumulative Sum (CUSUM) technique on the entropy sequence to find exactly where a significant shift occurs between successive entropy values and thus to signal concept change.

<br />
1. python (3.0)

**Usage**
======

$ make

if Make is not installed
------------------------
$ python3 main.py


**Notes**
=====

1. Make sure "dataset" folder have the associated data files
2. Go to "src" folder and run following commands:
    -make clean
    -make
    -make install
3. This code implements following paper:
    Yao, Yibo, and Lawrence B. Holder. "Detecting concept drift in classification over streaming graphs." KDD Workshop on Mining and Learning with Graphs (MLG), San Francisco, CA. 2016.

