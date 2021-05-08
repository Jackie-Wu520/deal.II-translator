# deal.II-translator
Using Doxygen format to translate packages into different languages-https://www.dealii.org/

- 首先，我们利用"./to.py filename" 生成剔除特殊字符的中转文件；
- 然后，利用deepl或者google翻译；
- 最后，利用"./from.py filename_0_T.txt";

可能用到的批量操作代码：
awk '/\[2.x.0\]/{n++;w=1} n&&w{print >"step-"n"_0_T.txt"}' T.txt
