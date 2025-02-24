## 设计要点
- 极简

### 作业模块
- 输入：自然语言输入，自动识别课程，作业，ddl，支持多个输入
- 输出：
  - TUI
  - GUI


## Usage
> Step 0: 配置环境
```
git clone https://github.com/Achyutace/auto-ddl-manager.git
cd auto-ddl-manager
pip install -r requirements.txt
```

> Step 1: 填写配置信息
> 在config_example.yaml中填写api_key，api_base和api_model，并改名为config.yaml

> Step 2: 启动
```
python main.py
```
