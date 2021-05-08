# deal.II-translator
Using Doxygen format to translate packages into different languages-https://www.dealii.org/

- 首先，我们利用"./to.py filename" 生成剔除特殊字符的中转文件；
- 然后，利用deepl或者google翻译；
- 然后，利用"./from.py filename_0_T.txt";
- 然后，得到的替换文件回代到source中，再一次进行编译。注意编译需要开启mathjax，否则公式可能乱码"cmake -DDEAL_II_COMPONENT_DOCUMENTATION=ON -DDEAL_II_DOXYGEN_USE_MATHJAX=ON",然后再输入"make documentation"，若有改动，只需输入后者，无需重头开始编译。

可能用到的批量操作代码：
- 拆分一次性翻译的文档：
awk '/\[2.x.0\]/{n++;w=1} n&&w{print >"step-"n"_0_T.txt"}' T.txt
- 重新批量命名
for file in `ls *.h`;do mv $file `echo $file|sed 's/_0_T//g'`;done;
- 批量允许python代码
for filename in headers/*.h; do
        ./to.py "$filename" 
done
for filename in examples/*_T.txt; do
        ./from.py ${filename} 
done
