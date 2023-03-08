python -m cProfile -o profiling/output.pstats -m consensus_pledge_model
gprof2dot --colour-nodes-by-selftime -f pstats profiling/output.pstats | \
    dot -Tpng -o profiling/output.png

