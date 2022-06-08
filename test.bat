cls
python src/compiler.py ./test/test.cod
gcc ./test/test.c -o ./test/test
"./test/test.exe"