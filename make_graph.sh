#! /bin/bash
rm output.pstats
rm output.png
python2.5 -m profile -o output.pstats speed_test.py 
./gpro2dot.py -f pstats output.pstats |dot -Tpng -o output.png
#xview output.png

