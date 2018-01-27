cpp程序通过命令行输入参数示例

./main sample test 20
int main(int argc, char **argv) {
    argc == 4
    argv[0] == "./main"
    argv[1] == "sample"
    num == atoi(argv[3])//转化成int
    ...
 }
