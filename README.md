<p>ZeRO和激活重算可以分别对静态显存(包括模型参数、梯度、优化器)和动态显存(中间激活 值)进行优化;</p><br><br><br>


**运行环境**：4090*2    48G显存<br>
**模型**：deepseek-math-7b<br><br>

<p>
case0：不开zero,    ---配置文件ds_z0.json<br>
case1：zero-1，切分优化器，    ---配置文件ds_z1.json<br>
case2：zero-2，切分优化器+梯度，    ---配置文件ds_z2.json;<br>
case3：zero-3，切分优化器+梯度+模型参数(全切分)    ---配置文件ds_z3.json<br>
case4：zero-3+激活重算，切分优化器+梯度+模型参数(全切分)    ---配置文件ds_z3.json<br>
case5：zero-2+激活重算+offload，切分优化器+梯度+offload    ---配置文件offload/ds_z2.json<br>
case6：zero-3+激活重算+offload，切分优化器+梯度+模型参数(全切分)+offload    ---配置文件offload/ds_z3.json<br><br><br>


**运行结果：<br>**
case0：OOM，<br>
case1：OOM,提示还差12.87G<br>
case2：OOM,提示还差10G<br>
case3：OOM,提示还差3G<br>
case4：OOM,提示还差2.5G<br>
case5：OOM,提示还差1.56G<br>
case6：successful<br>
</p>
