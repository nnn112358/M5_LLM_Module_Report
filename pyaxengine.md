# pyaxengine

AXモデルをPythonから実行できるライブラリ。


```
root@m5stack-LLM:# wget https://github.com/AXERA-TECH/pyaxengine/releases/download/0.0.1rc1/axengine-0.0.1-py3-none-any.whl
root@m5stack-LLM:# pip install axengine-0.0.1-py3-none-any.whl
root@m5stack-LLM:# pip install pillow
root@m5stack-LLM:# git clone https://github.com/AXERA-TECH/pyaxengine
root@m5stack-LLM:# cd pyaxengine/
root@m5stack-LLM:# AXERA-TECH/pyaxengine/examples/
root@m5stack-LLM:# python3 classification.py
[INFO] Chip type: ChipType.MC20E
[INFO] Engine version: 2.6.3sp
[INFO] VNPU type: VNPUType.DISABLED
[INFO] Model type: 0 (half core)
[INFO] Compiler version: 1.8-beta1 6a7e59de
Top 5 Predictions:
Class Index: 282, Score: 9.641450881958008
Class Index: 281, Score: 8.320703506469727
Class Index: 278, Score: 8.056554794311523
Class Index: 285, Score: 7.924480438232422
Class Index: 277, Score: 7.79240608215332
```

## 参考

AXERA-TECH/pyaxengine<br>
https://github.com/AXERA-TECH/pyaxengine<br>

M5Stack Module LLMのpython用runtimeのデモを動かす<br>
https://zenn.dev/airpocket/articles/3ae46a450a87be<br>
