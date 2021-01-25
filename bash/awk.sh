ex1:
abc def 123
dfg jik 234

awk '{print $2}'
o:
def
jik

ex2 data.txt:
Beth	4.00	0
Dan	3.75	0
kathy	4.00	10
Mark	5.00	20
Mary	5.50	22
Susie	4.25	18

awk '$3>0 { print $, $2 * $3 }' data.txt
o:
Kathy 40
Mark 100
Mary 121
Susie 76.5

#制定分隔符
-F ':'
