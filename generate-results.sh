for i in orig best-avg simplified leading; do for a in 1-1 1-2 1-3 1-4 2-1 2-2 2-3 2-4 3-1 3-2 3-3 3-4 4-1 4-2 4-3 4-4; do python sumbasic.py $i docs/doc$a.txt > results/docs$a-$i.txt; done; done;
