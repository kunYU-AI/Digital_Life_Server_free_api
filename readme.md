# Digital Life Server
B站极客湾「数字生命」的服务器代码的免费API KEY版本，因为原有的API KEY已经无法使用。  
如何具体实现AI派蒙的制作，请参看视频：[]()

除该github代码外，另需完成以下任务：
1. 获取客户端（Client）的文件夹：[极客湾提供的测试版文件中的Client文件夹](https://www.123pan.com/s/MjA7Vv-m82i.html)。
2. 获取免费的API KEY：[申请地址](https://github.com/chatanywhere/GPT_API_free)。
3. 确保电脑有python版本3.10（最稳妥）和Git。
4. 搭建虚拟环境和各种依赖：见下面指引。
5. 导入模型文件：[百度网盘](https://pan.baidu.com/s/1EnHDPADNdhDl71x_DHeElg?pwd=75gr)  
   ASR Model:
   to `/ASR/resources/models`  
   Sentiment Model:  
   to `/SentimentEngine/models`  
   TTS Model:  
   to `/TTS/models`
6. 启动虚拟环境、服务器和客户端，即可开启旅途（见下面指引）。

## 步骤4：搭建虚拟环境和各种依赖:
> ⚠ 注意：  
> 如果不知道你在干什么（纯小白），请在**需要存放该项目的位置**打开终端(Win11)或Powershell(win10)，然后**按照下述说明逐步操作**即可  
> 在进行以下操作前，请确保电脑中有Git和Python>=3.8（最好3.10）

### 克隆这个远程库代码
```bash
git clone https://github.com/kunYU-AI/Digital_Life_Server_free_api.git --recursive
cd Digital_Life_Server_free_api
```
如果失败，可以不使用recursive参数，依次克隆该远程库和`TTS/vits`的远程库。

### 配置环境
1. 使用virtualvenv建立python虚拟环境
   ```bash
   python -m venv venv
   ```
2. 安装pytorch于venv

   > 你可以在终端(或Powershell)输入`nvcc --version`，找到输出中`Cuda compilation tools`一行来查看cuda版本。或者

   对于cuda11.8： 

   （默认地址，下载可能较慢）
   ```bash
   .\venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
   （国内加速地址，下载可能较快）
   ```bash
   .\venv\Scripts\python.exe -m pip install torch==2.0.0+cu118 torchvision torchaudio -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html
   ```

   对于没有Nvidia显卡的电脑：

   （默认地址，下载可能较慢）
   ```bash
   .\venv\Scripts\python.exe -m pip install torch torchvision torchaudio
   ```
   （国内加速地址，下载可能较快）
   ```bash
   .\venv\Scripts\python.exe -m pip install torch==2.0.0+cpu torchvision torchaudio -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html

   ```
   其余版本组合可以从[这个页面](https://pytorch.org/get-started/locally)获取具体的下载指令  
3. 安装项目所需其它依赖项
   ```bash
   .\venv\Scripts\python.exe -m pip install -r requirements_out_of_pytorch.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
4. Build `monotonic_align`
   ```bash
   cd "TTS/vits/monotonic_align"
   mkdir monotonic_align
   python setup.py build_ext --inplace
   cp monotonic_align/*.pyd .
   ```
5. （对于**没有**Nvidia显卡的电脑，采用cpu来跑的话）需要额外做一步：将Digital_Life_Server_free_api\TTS\TTService.py 文件下 36行

   ```
   self.net_g = SynthesizerTrn(...).cuda()
   修改为
   self.net_g = SynthesizerTrn(...).cpu()
   ```
> 到这里，环境构建完毕🥰

## 步骤6：启动
> ⚠ 注意：  
> 启动前，不要忘记根据实际情况修改bat文件中的具体配置
```bash
run-gpt3.5-api.bat
```