+	加
-	减
*	乘
/	除
%	取模
因为Shell中将*作为通配符使用,所以使用\*转义

expr命令
expr命令可以对整数进行算术运算，在算术表达式中如果出现变量，必须在变量前加$，并且要在运算符和变量之间要加空格
expr空格9空格+空格$a

a=2
expr $a \* 2
b=`expr $a / 2`
echo $b

let命令
let命令可以进行算术运算，将算术表达式跟在let后面就可以实现数值的运算

b=10
let c=$b+2
echo $c
