# PythonProject - hw01（N 皇后/八皇后）

本仓库用 **Cursor** 作为 AI 编程工具，完成 `hw01` 的 Python 工程搭建、N 皇后（八皇后）求解器实现与测试。


## 目录结构

- `hw01/`
  - `src/hw01/`：源码（求解器实现）
  - `tests/`：pytest 测试
  - `pyproject.toml`：项目与测试配置

## 如何使用 Cursor 实现本项目

### 0. 在 Cursor 中打开工程

- 用 Cursor 打开仓库根目录（`E:\pythonFiles\PythonProject`）。
- 确认左侧文件树能看到 `hw01/`。

### 1. 让 Cursor 生成工程骨架（目录 + 基础文件）

在对话里描述你的期望结构，例如：

- “我要在 `hw01` 目录下构建一个 python 工程，包含 `src` 源码目录和 `tests` 测试目录。”

你期望 Cursor 输出并生成类似结构：

- `hw01/src/hw01/__init__.py`
- `hw01/tests/`
- `hw01/pyproject.toml`
- `hw01/README.md`


### 2. 让 Cursor 实现 N 皇后（八皇后）求解器 + 测试

继续在对话里明确功能与测试目标，例如：

- “请实现八皇后求解器，并写对应的测试。”

一个可测的接口设计建议（本项目采用）：

- `solve_n_queens(n)`：返回所有解（每个解用 `solution[row] = col` 表示）
- `is_valid_solution(solution)`：验证解合法性
- `format_solution(solution)`：将解渲染成棋盘字符串


### 3. 在 Cursor 内运行与验证（Terminal）

在 Cursor 的 Terminal 里进入 `hw01`，安装并运行。

#### 3.1 运行求解器（示例）

```bash
cd E:\pythonFiles\PythonProject\hw01
python -m pip install -e .
python -c "from hw01.nqueens import solve_n_queens,format_solution; s=solve_n_queens(8); print(len(s)); print(format_solution(s[0]))"
```

期望输出：第一行是 `92`（8 皇后解数量）。


#### 3.2 运行测试（pytest）

```bash
cd E:\pythonFiles\PythonProject\hw01
python -m pip install -e \".[dev]\"
python -m pytest
```

期望：全部通过。


### 4. 出问题时，如何用 Cursor 协助定位并修复

推荐提问方式：把“**失败用例 + 报错堆栈 + 你期望的行为**”贴给 Cursor，例如：

- “现在我的测试出现问题了，你帮我查找问题在哪？这是 pytest 输出：……”

#### 示例：制造并修复一个 bug

例如在 `is_valid_solution()` 里写错列范围校验：

- 正确：`0 <= c < n`
- 错误（会把第 0 列误判为非法）：`0 < c < n`

一旦出现失败，把 pytest 的失败输出贴出来，让 Cursor：

- 复现失败
- 定位到具体函数/行
- 给出最小修复
- 重新跑测试确认全绿

## 本项目关键命令速查

在 `hw01` 目录下：

- **安装（可运行）**：`python -m pip install -e .`
- **安装（含测试依赖）**：`python -m pip install -e ".[dev]"`
- **运行测试**：`python -m pytest -q`
