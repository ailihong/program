for i in `ls temp/*.txt` #temp/1.txt,temp/2.txt
do
    #mkdir ./${i%.tar}
    #tar xvf $i -C ./${i%.tar}
    echo ${i} #print the whole name,example:temp/1.txt
    echo ${i%.txt} #exclude the txt,example:temp/1
    echo debug/`basename ${i}` #out:debug/1.txt
done

for i in aa bb cc
do
    echo ${i}#print aa,bb,cc
done
