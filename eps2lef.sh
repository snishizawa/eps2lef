#!/bin/sh

#python3 eps2lef.py -i GateArraySC/INV_GA2.eps -n INV_GA -l INV_GA2.lef
python3 eps2lef.py -i layout/DFFAR_1X.eps -n DFFAR_1X -l lef/DFFAR_1X.lef
python3 eps2lef.py -i layout/INV_1X.eps -n INV_1X -l lef/INV_1X.lef
python3 eps2lef.py -i layout/NAND2_1X.eps -n NAND2_1X -l lef/NAND2_1X.lef
python3 eps2lef.py -i layout/NAND3_1X.eps -n NAND3_1X -l lef/NAND3_1X.lef
python3 eps2lef.py -i layout/NAND4_1X.eps -n NAND4_1X -l lef/NAND4_1X.lef
python3 eps2lef.py -i layout/NOR2_1X.eps -n NOR2_1X -l lef/NOR2_1X.lef
python3 eps2lef.py -i layout/NOR3_1X.eps -n NOR3_1X -l lef/NOR3_1X.lef
python3 eps2lef.py -i layout/NOR4_1X.eps -n NOR4_1X -l lef/NOR4_1X.lef
