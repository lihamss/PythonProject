# Python项目目录构建与八皇后问题
_Exported on 2026/3/11 at GMT+8 16:04:58 from Cursor (2.5.22)_

---

**User**

我要在hw01目录下构建一个python工程，包含src源码目录和tests测试目录，之后我要实现八皇后问题的求解器，你先构建我要的项目目录

---

**Cursor**

我先检查一下仓库里是否已经有 `hw01`（避免覆盖），然后用最小但可运行的工程骨架把目录和基础文件一次性创建出来：`hw01/src/`、`hw01/tests/`，并补上 `pyproject.toml`、`README.md`、pytest 配置与包初始化文件。

确认当前还没有 `hw01` 目录；接下来我会直接创建工程骨架文件（这些文件的路径会自动带出你要的目录结构），完成后再快速核对目录树是否符合预期。

已在 `hw01` 下把你要的 Python 工程骨架建好了，目录结构如下：

- `hw01/README.md`
- `hw01/pyproject.toml`
- `hw01/.gitignore`
- `hw01/src/hw01/__init__.py`
- `hw01/tests/__init__.py`

接下来你可以直接在 `hw01/src/hw01/` 里实现八皇后求解器代码，在 `hw01/tests/` 里写对应测试。

---

**User**

好的，请你实现八皇后求解器，并写对应的测试

---

**Cursor**

我会先把求解器接口设计成简单可测的函数（例如 `solve_n_queens(n)` 返回所有解），然后用回溯 + 位运算实现高效求解；最后补上 pytest 测试，覆盖典型 \(n=1/4/8\) 和无解 \(n=2/3\) 的情况，并验证每个解都满足不冲突约束。

求解器核心代码已落到 `src/hw01/nqueens.py`：用位掩码回溯生成所有解，并提供了解的校验与格式化函数。接下来我会把这些接口从包里导出，然后补上 pytest 测试用例并实际跑一遍测试。

代码和测试都写好了，静态检查也没问题；现在失败的原因只是你当前环境还没装 `pytest`。我接下来会在 `hw01` 这个工程里安装开发依赖（`.[dev]`），然后重新跑测试，确保八皇后（\(n=8\)）得到 92 个解且全部合法。

## 已完成：八皇后（N 皇后）求解器 + 测试

### 实现内容
- **求解器模块**：`hw01/src/hw01/nqueens.py`
  - `solve_n_queens(n)`：返回所有解（每个解是长度为 n 的元组，`solution[row]=col`）
  - `iter_n_queens_solutions(n)`：生成器版本
  - `is_valid_solution(solution)`：校验解合法性
  - `format_solution(solution)`：把解格式化成棋盘字符串
- **包导出**：已在 `hw01/src/hw01/__init__.py` 导出上述接口
- **测试**：`hw01/tests/test_nqueens.py`
  - 覆盖 `n=0/1/2/3/4/8` 的解数量（8 皇后应为 **92**）
  - 校验所有解都合法且不重复
  - 校验迭代器与一次性求解结果一致
  - 校验格式化输出基本正确
  - 校验非法 n 会抛异常

### 运行结果
在 `hw01` 下运行 `python -m pytest -q`：**10 passed**。

---

**User**

我要如何运行八皇后求解器以及如何使用测试脚本

---

**Cursor**

## 运行八皇后求解器

在项目目录执行（先进入 `hw01`）：

```bash
cd E:\pythonFiles\PythonProject\hw01
python -m pip install -e .
```

然后在 Python 里调用：

```bash
python
```

```python
from hw01.nqueens import solve_n_queens, format_solution

sols = solve_n_queens(8)
print(len(sols))                 # 92
print(format_solution(sols[0]))  # 打印第一组解的棋盘
```

也可以一行命令直接跑：

```bash
python -c "from hw01.nqueens import solve_n_queens,format_solution; s=solve_n_queens(8); print(len(s)); print(format_solution(s[0]))"
```

## 使用测试脚本（pytest）

安装测试依赖并运行（在 `hw01` 下）：

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

想看更简洁输出：

```bash
python -m pytest -q
```

---

**User**

现在我的测试出现问题了，你帮我查找问题在哪？

---

**Cursor**

我先在你当前 `hw01` 工程目录里直接把测试跑一遍，抓到**具体失败用例与报错堆栈**；然后再回到对应源码/测试文件逐行定位原因并修复，最后再次跑到全绿为止。

失败点很集中：`solve_n_queens(4)` 给出的经典解 `(1, 3, 0, 2)` 被 `is_valid_solution` 判成了非法，因此 8 皇后的“全部解都合法”也连带失败。接下来我会直接检查 `is_valid_solution` 的逻辑（大概率是类型判断或对角线集合处理写错/被改动），并用最小改动修复后重跑测试。

定位到了根因：`is_valid_solution` 把列范围写成了 `0 < c < n`，导致 **第 0 列永远被判非法**，所以像 `(1,3,0,2)` 这种含 0 的正确解会失败。我已经把它修正为 `0 <= c < n`，接下来立刻重跑测试确认全绿。

## 问题原因
`hw01/src/hw01/nqueens.py` 里的 `is_valid_solution()` 把列范围写成了 `0 < c < n`，**错误地排除了第 0 列**，所以像 `(1, 3, 0, 2)` 这种正确解会被判为非法，进而导致你的 8 皇后合法性断言失败。

我已把它修正为 `0 <= c < n`。

## 结果
现在在 `hw01` 下运行：

```bash
python -m pytest -q
```

已恢复为 **10 passed**。

