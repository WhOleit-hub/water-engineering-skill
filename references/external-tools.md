# 外部工具参考 — HEC-RAS、MIKE 11 与水动力建模

> ⚡ **自动加载场景**：当用户提到 HEC-RAS、MIKE 11、水面线软件、洪水演进、非恒定流模拟、水力建模、洪水风险图时，Read 此文件。
>
> **定位**：国际主流水动力软件的操作指南。中国工程设计以中国规范为最终依据，HEC-RAS/MIKE 11 作为计算工具使用，成果合理性和参数选取应与中国规范校核。
>
> **核心前提**：水面线计算前，务必先完成 §0 铁律（读图确认水流路径）。错误的上下游关系→错误的数据→整节重做。

## 目录

- [HEC-RAS —— 河道水面线分析标准工具](#hec-ras--河道水面线分析标准工具)
  - [HEC-RAS 恒定流水面线完整操作流程](#hec-ras-恒定流水面线完整操作流程)
  - [桥梁壅水分析（防洪评价最常用场景）](#桥梁壅水分析防洪评价最常用场景)
  - [HEC-RAS 2D 洪泛区模拟](#hec-ras-2d-洪泛区模拟)
  - [HEC-RAS 常见问题与调试](#hec-ras-常见问题与调试)
- [MIKE 11 —— 全流域水文水动力一体化平台](#mike-11--全流域水文水动力一体化平台)
  - [MIKE 11 核心模块体系](#mike-11-核心模块体系)
  - [NAM 降雨径流模型参数率定](#nam-降雨径流模型参数率定)
  - [MIKE 11 完整建模流程](#mike-11-完整建模流程)
- [Python 水面线计算引擎（不依赖商业软件）](#python-水面线计算引擎不依赖商业软件)
  - [标准步推法逐段试算 — 完整实现](#标准步推法逐段试算--完整实现)
- [HEC-RAS vs MIKE 11 vs 远盛水工 vs Python 选型](#hec-ras-vs-mike-11-vs-远盛水工-vs-python-选型)

---

# HEC-RAS —— 河道水面线分析标准工具

> **开发商**：美国陆军工程兵团 (USACE) | **价格**：免费 | **版本**：当前 6.x
> **官网**：https://www.hec.usace.army.mil/software/hec-ras/
> **中文学习**：B站搜索"HEC-RAS 教程"大量实操视频

## HEC-RAS 能做什么

| 功能 | 描述 | 中国工程用途 |
|------|------|-------------|
| **恒定流水面线** (Steady Flow) | 输入 $Q$，推求各断面 $Z$ — 最常用 | 防洪评价壅水分析、堤顶高程确定 |
| **非恒定流** (Unsteady Flow) | 输入 $Q(t)$ 过程线，模拟洪水演进 | 河道洪水演进、水库调洪 |
| **泥沙输移** (Sediment) | 冲淤计算 | 较少用（国内其他软件为主） |
| **水质模拟** | DO/BOD/水温 | 水环境评价辅助 |
| **2D 洪泛区** (RAS 2D) | 二维洪水淹没模拟 | 洪水风险图绘制 |
| **桥涵分析** | 桥墩壅水、桥面过流 | **涉河工程防洪评价核心功能** |

## HEC-RAS 恒定流水面线完整操作流程

### 第一步：几何数据 (Geometric Data) — 最耗时，占70%工作量

```
1. 创建新项目 File → New Project
2. 进入几何数据编辑器 Edit → Geometric Data
3. 画河道中心线 (River)：
   - 点模式：从上游到下游画折线
   - 每拐一点左键确认，右键结束
   - 命名 River / Reach
4. 输入横断面 (Cross Section)：
   → 主菜单 Cross Section → Draw (或右键)
   → 每条断面输入：
      ┌─ 断面编号 (River Station)：如 1000, 900, 800...
      ├─ 距离下游 (Upstream Reach Lengths)：左/主/右三个方向
      ├─ 断面坐标：从左侧开始，输入 (距离, 高程) 点对
      ├─ 曼宁糙率：主槽 n_c、左滩 n_l、右滩 n_r
      └─ 主槽位置识别 (Bank Station)：左/右岸位置

5. 断面数据格式示例（文本输入方式）：
   ```
   # 断面号：500 (距起点500m)
   # 坐标点 (距起点距离, 高程)
   0.0    105.2
   15.0   104.8
   25.0   103.5  ← 左岸起点
   35.0   102.0  ← 左水边
   45.0   100.5
   55.0   99.8   ← 深泓点
   65.0   100.8
   75.0   102.5  ← 右水边
   88.0   104.0  ← 右岸终点
   100.0  105.5

   曼宁系数：n_l=0.04, n_c=0.03, n_r=0.04
   左岸 Bank Station = 30
   右岸 Bank Station = 80
   ```

6. 桥/涵/闸等建筑物（如需要）：
   → 在主菜单选择 Bridge/Culvert/Inline Structure
   → 在对应断面插入桥墩、涵洞或闸门参数
```

### 第二步：恒定流数据 (Steady Flow Data)

```
1. 进入 Edit → Steady Flow Data
2. 输入流量：
   ┌─ 所有断面输入栏：在 Profile 1 栏输入 Qp (如 Q1%=850m³/s)
   └─ 如有支流分流，在各断面分别输入
3. 添加计算方案：
   → Options → Add Profile
   └─ 命名：如 Q1%, Q2%, Q5%...
4. 设置边界条件 (Boundary Conditions)：
   ┌─ 下游断面（第一个边界）：
   ├─ 缓坡 → Known W.S.（已知水位）或 Normal Depth（曼宁计算）
   │          例：Normal Depth 时输入底坡 i=0.001
   ├─ 陡坡 → Critical Depth（临界水深）
   └─ 上游断面（可选）：Flow Hydrograph（非恒定流用）
```

**边界条件选择依据（最重要决策）：**

| 流态 | 下游边界 | 上游边界 | 说明 |
|------|---------|---------|------|
| 亚临界 (Fr<1) | ✅ 必设 | 可省略 | 缓坡河道最常见 |
| 超临界 (Fr>1) | 可省略 | ✅ 必设 | 陡坡/急流 |
| 混合流 | ✅ 必设 | ✅ 必设 | 过桥/跌水处流态变化 |

### 第三步：运行计算

```
1. Run → Steady Flow Analysis
2. 设置计算参数：
   └─ Flow Regime：
       Subcritical（亚临界）— 绝大多数情况
       Mixed（混合流）— 桥墩/跌水上下游
   └─ 其他保持默认
3. Compute → 计算完成
   └─ 若报错 → 查看 Computational Log 
```

### 第四步：结果查看与导出

```
1. 纵断面图：View → Profile Plot
   └─ 点选各计算 Profile → 看水面线
   └─ Options → Plot Series → 多 Profile 对比

2. 横断面水情：View → Cross Section
   └─ 逐断面看水位与断面关系

3. 详细数据表格：View → Detailed Output Table
   └─ 关键成果：各断面 Q / Z_min / Z_max / Velocity / Froude / E.G.

4. 导出：
   └─ 水面线成果 Excel: File → Export → To Excel
   └─ 断面图: View → Copy to Clipboard → 粘贴到报告
```

## 桥梁壅水分析（防洪评价最常用场景）

### 场景说明

某新建桥梁跨越河道，桥墩占用行洪断面，需计算壅水高度 $\Delta Z$。

### 操作序列

```
天然工况：
Step 1: 建立河道几何（无桥）→ 仅 River + Cross Sections
Step 2: 输入设计流量 Qp
Step 3: 运行计算 → 得天然水位 Z_天然

工程工况：
Step 4: 在桥址断面处插入 Bridge（Tools → Bridge Culvert）
          └─ 输入桥墩参数：墩宽、墩长、墩数、形状系数
          └─ 输入桥面高程（判断桥上过流/不过流）
Step 5: 同流量 Qp 计算 → 得工程水位 Z_工程

成果：
Step 6: 壅水高度 ΔZ = Z_工程 - Z_天然
Step 7: 壅水长度 L = 上游回水延伸距离（水面线与天然线交点）

输出到防洪评价报告 §5.2：
  └─ 各频率壅水高度 ΔZ
  └─ 壅水长度
  └─ 桥下净空高度校核
  └─ 冲刷深度复核
```

### 桥墩壅水参数速查

| 参数 | 经验值 | 说明 |
|------|--------|------|
| 桥墩形状系数 $K$ | 圆形 0.9 / 矩形 1.2 / 尖端形 0.7 | 越小水阻越小 |
| 收缩系数 $C_c$ | 0.6~1.0 | 桥面与河道宽度比 |
| Block 百分比 | 桥墩阻断面积/总过流面积 | HEC-RAS 自动计算 |

## HEC-RAS 2D 洪泛区模拟

### 适用场景
- 洪水风险图编制
- 溃坝洪水淹没范围
- 河道-洪泛区耦合模拟

### 快速入门

```
1. 在 Geometric Data 中：
   → RAS Mapper → Create New 2D Flow Area
   → 圈出洪泛区范围多边形
   → 设定网格尺寸（Cell Size）：一般 10~50m
         └─ 网格越小越精确，但计算时间指数增长

2. 连接 1D 河道与 2D 洪泛区：
   → 在河道断面处定义 Lateral Structure
   └─ 允许河道水漫过堤防进入 2D 区

3. 边界条件：
   → 上游入流：从 Steady/Unsteady 来
   → 下游出流：Normal Depth 或 潮位边界

4. 查看结果：
   → RAS Mapper → Flood Mapping
   └─ 生成淹没水深网格图
   └─ 导出为 .tif (GIS 可用)
```

## HEC-RAS 常见问题与调试

| 现象 | 原因 | 解决 |
|------|------|------|
| "The program encountered an error" | 断面数太少/间距不均 | 加密断面，确保 ≥5 个 |
| 水面线锯齿状震荡 | 断面形状突变/主槽Bank位置错 | 检查各断面 Bank Station 一致性 |
| 水位异常偏低（大Q小Z） | 断面未延伸到足够宽/高 | 断面要超过可能最高水位 |
| Flood Plain 流量占比异常 | Bank Station 设错 | 左右岸 Bank 应标记主槽边界 |
| 计算发散（不收敛） | 断面间距太大/迭代次数不够 | 减小 Critical Depth Tol 至 0.01 |
| 桥址附近水位突降 | 桥墩 Block 过大 | 检查桥墩几何和裙板高度 |
| 计算结果与实测偏差大 | 糙率 n 不对 | 用实测水位/流量率定 → 反算 n |
| 非恒定流不收敛 | Δt 太大 | 设为 Δt ≤ Δx / √(gh_max) |

---

# MIKE 11 —— 全流域水文水动力一体化平台

> **开发商**：丹麦水力研究所 (DHI) | **价格**：商业许可（~¥15-30万/年）
> **官网**：https://www.mikepoweredbydhi.com/ | **中文**：www.dhigroup.cn
> **学习资源**：DHI Academy 在线课程 + 自带的 Tutorial 文档

## MIKE 11 核心模块体系

```
MIKE 11 模块架构：
┌─────────────────────────────────────────────────────────────┐
│  RR (Rainfall-Runoff) 降雨径流                               │
│  ├─ NAM 模型：集总式概念模型，9参数                           │
│  ├─ UHM：单位线法（适用洪峰模拟）                              │
│  ├─ SMAP：土壤水分模型                                        │
│  └─ FEH：英国洪水估算方法                                     │
├─────────────────────────────────────────────────────────────┤
│  HD (Hydrodynamic) 水动力核心                                 │
│  ├─ 1D 圣维南方程组求解                                       │
│  ├─ 支持复杂河网（多支流/环状/闸泵堰）                        │
│  └─ 结构物控制规则（闸门调度/泵站启闭）                        │
├─────────────────────────────────────────────────────────────┤
│  AD (Advection-Dispersion) 对流扩散 — 水质/水温/盐度          │
│  ST (Sediment Transport) 泥沙输移                             │
│  FF (Flood Forecasting) 洪水预报 + 实时校正                    │
└─────────────────────────────────────────────────────────────┘
```

### HEC-RAS 与 MIKE 11 核心定位差异

**HEC-RAS = 河道水力计算器**
- 你把 $Q_p$ 算好给它 → 它输出 $Z_p$
- 只管河道水力，不管流域产汇流
- 恒定流模式：水面线一把算出，是最常用场景

**MIKE 11 = 流域水文水动力模拟器**
- 你给降雨 → RR 模型算 $Q(t)$ → HD 算 $Z(t)$
- 河道+流域一体化，能用降雨直接算出洪水位全过程
- 核心优势：**NAM 模型的产汇流能力 HEC-RAS 没有**

## NAM 降雨径流模型参数率定

NAM 是 MIKE 11 产汇流模块最常用的模型，9个核心参数决定模拟成败。

### 参数表

| 参数 | 含义 | 单位 | 典型范围 | 对结果的影响 |
|------|------|------|---------|-------------|
| Umax | 地表蓄水容量 | mm | 10~25 | **峰量** — 越大洪峰越低 |
| Lmax | 根层蓄水容量 | mm | 50~250 | **基流** — 影响雨季/旱季过渡 |
| CQOF | 地表径流系数 | — | 0.3~0.9 | **水量** — 影响总径流量最大 |
| CKIF | 壤中流排水常数 | h | 100~2000 | **退水** — 控制退水段形状 |
| CK1 | 地表径流时间常数(坡面) | h | 10~50 | **洪峰滞后** — 峰现时间 |
| CK2 | 地表径流时间常数(河道) | h | 10~50 | **峰形** — 过程线拖尾形状 |
| Tg | 根层补水触发阈值 | mm | 0~10 | **产流时机** — 雨季开始 |
| K_IF | 壤中流排水系数 | mm/h | 0.1~1.0 | **退水速率** |
| K_BF | 基流排水系数 | mm/h | 0.001~0.1 | **枯水期形态** |

### 率定流程（六步法）

```
第一步：数据准备
   输入：实测降雨 P(t) + 蒸发 E(t) + 流量 Q_obs(t)
   要求：≥3年日序列，其中2年率定、1年验证

第二步：默认参数跑一轮
   输出 Q_sim(t) 与 Q_obs(t) 对比图
   关注：总水量偏差、峰现时间、退水段

第三步：先调水量（CQOF + Umax + Lmax）
   总径流偏大 → 增大 CQOF
   总径流偏小 → 减小 CQOF（CQOF = 0.3~0.9）
   洪峰偏尖 → 增大 Umax

第四步：调峰现时间（CK1 + CK2）
   峰现偏早 → 增大 CK1（坡面汇流变慢）
   峰现偏晚 → 减小 CK1

第五步：调退水段（CKIF + K_BF）
   退水太快 → 增大 CKIF
   退水太慢 → 减小 CKIF

第六步：计算指标
   目标：NSE ≥ 0.7，水量偏差 < ±10%
   NSE = 1 - Σ(Q_obs - Q_sim)² / Σ(Q_obs - Q_mean)²

   验证期用另一年份数据跑 → NSE ≥ 0.6 可接受
```

## MIKE 11 完整建模流程

### 文件体系

MIKE 11 的一个完整模型由 5 个独立文件组成：

```
项目文件夹/
├── river.nwk11       ← 河网文件（河道中心线 + 节点连接）
├── cross.xns11       ← 断面文件（各桩号横断面坐标）
├── boundary.bnd11    ← 边界条件（上下游 + 侧向入流）
├── parameter.rr11    ← RR 参数文件（NAM 模型参数）
├── simulation.sim11  ← 模拟控制文件（时间步长/时段/模块选择）
└── *.dfs0            ← 时间序列数据（降雨/蒸发/实测流量）
```

### 操作流程

```
Step 1. 河网文件 (.nwk11)
   → 在 MIKE Zero 中创建/编辑
   → 画河道线 + 设河段长度
   → 定义交汇点连接关系
   → 可导入 Shapefile / DXF

Step 2. 断面文件 (.xns11)
   → 在 Cross Section Editor 中输入
   → 格式与 HEC-RAS 类似：(X, Z) 点对
   → 定义曼宁系数 n（可随水位变化）
   └─ MIKE 11 优势：n 可设为水深函数

Step 3. NAM 参数文件 (.rr11)
   → 在 RR Editor 中设置
   → 子流域划分 → 每个子流域一套 NAM 参数
   → 链接时间序列(.dfs0)作为输入

Step 4. 边界条件 (.bnd11)
   → 上游边界：实测入流 / NAM 产流输出 / 流量过程线
   → 下游边界：实测水位 / 潮位 / Q-h 关系 / 曼宁公式
   → 侧向入流：子流域 NAM 计算后自动汇入

Step 5. 模拟参数 (.sim11)
   → 时间步长 Δt：一般 30~300s（取决于 CFL 条件）
   → HD 参数：θ=0.6~0.8（时间加权系数）
   → 模拟时段：起始/结束时间

Step 6. 运行 + 结果
   → 逐断面水位过程线 Z(t)
   → 逐断面流量过程线 Q(t)
   → 最大洪水位包络图
   → 动画展示洪水演进
```

---

# Python 水面线计算引擎（不依赖商业软件）

用户提供实测横断面数据时，用以下 Python 代码直接计算水面线。

## 标准步推法逐段试算 — 完整实现

```python
import numpy as np
import pandas as pd

def standard_step_method(
    sections,       # 断面列表，每个断面为 dict:
                    #   {'z': [高程数组], 'x': [距起点距数组], 
                    #    'station': 桩号, 'n_c': 主槽糙率,
                    #    'n_l': 左滩糙率, 'n_r': 右滩糙率,
                    #    'bank_left': 左岸位置, 'bank_right': 右岸位置}
    Q,              # 设计流量 (m³/s)
    i,              # 河道底坡
    h_downstream,   # 下游起推水深 (m)
    z_bed_down,     # 下游断面河底高程 (m)
    g=9.81,         # 重力加速度
    max_iter=50,    # 最大迭代次数
    tol=0.01        # 收敛容差 (m)
):
    """
    标准步推法计算水面线（适用于天然河道任意断面）
    
    返回每个断面的水位 Z、水深 h、流速 V、Fr、断面信息
    """
    n = len(sections)
    results = []
    
    def calc_hydro(section, water_level):
        """给定水位，计算过水面积A、湿周P、水力半径R"""
        z = np.array(section['z'])
        x = np.array(section['x'])
        bl = section['bank_left']
        br = section['bank_right']
        
        A, P = 0.0, 0.0
        # 逐段梯形积分求过水面
        for i in range(len(x)-1):
            x1, x2 = x[i], x[i+1]
            z1, z2 = z[i], z[i+1]
            dx = x2 - x1
            # 判断该段是否在水下
            if water_level > z1 or water_level > z2:
                # 水下高度
                h1 = max(0, water_level - z1)
                h2 = max(0, water_level - z2)
                if h1 > 0 and h2 > 0:
                    # 完全淹没
                    A += (h1 + h2) / 2 * dx
                    P += np.sqrt(dx**2 + (z2 - z1)**2) if dx > 0 else 0
                elif h1 > 0 and h2 <= 0:
                    # 部分淹没(1侧)
                    frac = h1 / (z1 - z2) if (z1-z2) > 0 else 1
                    frac = min(1, frac)
                    A += 0.5 * h1 * dx * frac
                    P += np.sqrt((dx*frac)**2 + h1**2) if dx > 0 else 0
                elif h2 > 0 and h1 <= 0:
                    frac = h2 / (z2 - z1) if (z2-z1) > 0 else 1
                    frac = min(1, frac)
                    A += 0.5 * h2 * dx * frac
                    P += np.sqrt((dx*frac)**2 + h2**2) if dx > 0 else 0
        
        R = A / P if P > 0 else 0.001
        return A, P, R
    
    # 从下游向上游逐段推进
    for idx in range(n-1, -1, -1):
        sec = sections[idx]
        
        if idx == n-1:
            # 下游控制断面
            h = h_downstream
            A, P, R = calc_hydro(sec, z_bed_down + h)
            V = Q / A if A > 0 else 0
            Fr = V / np.sqrt(g * (A / (sec['bank_right'] - sec['bank_left'])))
            E = (z_bed_down + h) + V**2 / (2*g)
            
            results.insert(0, {
                'station': sec['station'],
                'water_level': z_bed_down + h,
                'depth': h,
                'area': A,
                'velocity': V,
                'froude': Fr,
                'energy': E
            })
            continue
        
        # 上游断面 — 迭代求解
        prev = results[0]  # 刚求出的下游断面
        ds = abs(sec['station'] - sections[idx+1]['station'])
        
        z_bed_up = np.min(sec['z'])
        h_guess = prev['depth'] + i * ds  # 初始假设
        
        for _ in range(max_iter):
            wl = z_bed_up + h_guess
            A_up, P_up, R_up = calc_hydro(sec, wl)
            V_up = Q / A_up if A_up > 0 else 0
            Fr_up = V_up / np.sqrt(g * (A_up / (sec['bank_right'] - sec['bank_left'])) if A_up > 0 else 0.001)
            
            # 水力坡降（平均）
            n_up = sec['n_c']
            J_up = (n_up * V_up / (R_up**(2/3)))**2 if R_up > 0 else 0
            J_down = prev.get('J', J_up)
            J_avg = (J_up + J_down) / 2
            
            E_up = wl + V_up**2 / (2*g)
            E_down = prev['energy']
            
            # 步推公式：ΔE = (i - J_avg) * Δs
            E_calc = E_down + (i - J_avg) * ds
            
            diff = E_up - E_calc
            if abs(diff) < tol:
                break
            # 调整水深
            dh = diff * 0.5  # 阻尼因子
            h_guess -= dh
            h_guess = max(0.1, h_guess)
        
        if Fr_up > 1:
            print(f"⚠️ 断面 {sec['station']}: Fr={Fr_up:.3f} > 1，超临界流")
        
        results.insert(0, {
            'station': sec['station'],
            'water_level': wl,
            'depth': h_guess,
            'area': A_up,
            'velocity': V_up,
            'froude': Fr_up,
            'energy': E_up,
            'J': J_up
        })
    
    return results

def print_profile(results):
    """打印水面线结果表格"""
    print(f"\n{'桩号':>8} {'水位(m)':>10} {'水深(m)':>8} {'流速(m/s)':>10} {'Fr':>8} {'过流面积':>10}")
    print('-' * 60)
    for r in results:
        print(f"{r['station']:>8.0f} {r['water_level']:>10.3f} {r['depth']:>8.3f} "
              f"{r['velocity']:>10.3f} {r['froude']:>8.3f} {r['area']:>10.2f}")

def plot_profile(results, sections, title="水面线纵断面"):
    """绘制水面线与河底线"""
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    stations = [r['station'] for r in results]
    wl = [r['water_level'] for r in results]
    bed = [r['water_level'] - r['depth'] for r in results]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # 水面线图
    ax1.plot(stations, wl, 'b-', linewidth=2, label='水面线')
    ax1.plot(stations, bed, 'k-', linewidth=1.5, label='河底线')
    ax1.fill_between(stations, bed, wl, alpha=0.3, color='cyan')
    ax1.set_xlabel('桩号 (m)')
    ax1.set_ylabel('高程 (m)')
    ax1.set_title(title)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 流速图
    vel = [r['velocity'] for r in results]
    ax2.bar(stations, vel, width=ds*0.6, alpha=0.6, color='orange')
    ax2.set_xlabel('桩号 (m)')
    ax2.set_ylabel('流速 (m/s)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig
```

### 断面数据准备格式

用户按以下 CSV 格式提供断面数据即可：

```csv
station,z_bed,left_bank,right_bank,n_main,n_left,n_right,bottom_slope
1000,105.2,30,80,0.030,0.040,0.040,0.001
900,104.5,28,78,0.030,0.040,0.040,0.001
800,103.8,32,82,0.030,0.040,0.040,0.001
700,103.0,30,80,0.030,0.050,0.050,0.001
600,102.3,28,78,0.030,0.040,0.040,0.001
500,101.5,30,80,0.035,0.045,0.045,0.001
```

断面坐标点（每个断面单独 CSV）：

```csv
# 断面 1000 的坐标点
x,z
0,107.5
15,106.8
30,105.2
40,103.0
50,101.5
60,103.2
70,105.0
80,105.8
100,107.0
```

### 使用示例

```python
# 用户提供断面数据 → 一键算水面线
sections = [
    {'station': 1000, 'z': [107.5,106.8,105.2,103.0,101.5,103.2,105.0,105.8,107.0],
     'x': [0,15,30,40,50,60,70,80,100],
     'bank_left': 30, 'bank_right': 80,
     'n_c': 0.03, 'n_l': 0.04, 'n_r': 0.04},
    # ... 更多断面
]
results = standard_step_method(sections, Q=850, i=0.001, h_downstream=2.5, z_bed_down=101.5)
print_profile(results)
```

---

# HEC-RAS vs MIKE 11 vs 远盛水工 vs Python 选型

| 需求 | 推荐工具 | 理由 |
|------|---------|------|
| 防洪评价壅水计算（桥梁/码头） | **HEC-RAS** | 免费、评审认可、操作简单 |
| 河道水面线（没预算买软件） | **Python** | 零成本，可控，可批量计算 |
| 多频率(Q1%/Q2%/Q5%)批量水面线 | **HEC-RAS** | 多 Profile 同时计算 |
| 复杂河网（多支流+闸/泵） | **MIKE 11** | 河网耦合能力强 |
| 流域洪水模拟（降雨→洪水过程） | **MIKE 11** | NAM 模型产汇流 |
| 洪水风险图（二维淹没） | **HEC-RAS 2D** | 免费，功能足够 |
| 快速出图出计算书 | **远盛水工** | CAD+计算一体化 |
| 参数敏感性分析+批量试算 | **Python** | 自动循环最适合 |

### 典型组合流程

```
防洪评价项目 ─ 推荐工作流：

  ① P-III 频率分析 → 设计洪峰 Qp
     ↓ (工具：Python §4.5 或 Excel)
  ② HEC-RAS 水面线计算 → 各断面设计水位 Zp
     ↓ (工具：HEC-RAS Steady Flow)
  ③ 成果整理 → 防洪评价报告
     ↓ (工具：Python 出图 + Word)
     
  ④ 复杂桥墩处 → HEC-RAS Bridge 精细化模拟
     ↓
  ⑤ 必要时 → HEC-RAS 2D 验证壅水影响范围
```

---

# 附录：HEC-RAS 7.0 文件格式与技巧

> 以下内容来自实战验证（2026年6月），适用于 HEC-RAS 7.x

## HEC-RAS 7.0 几何文件 (.g01) 正确格式

从 `ras-commander` 模板库逆向得到的格式，与 HEC-RAS 4.x/5.x 的旧格式不兼容。

### 文件头

```
Geom Title=项目名称
Program Version=7.00
Viewing Rectangle= 1.79769313486232E+308 , 1.79769313486232E+308 , 1.79769313486232E+308 , 1.79769313486232E+308 
```

### 河道定义

```
River Reach=河道名             ,河道名             
Reach XY= 2 
             0.5             0.8             0.5             0.2
Rch Text X Y=,
Reverse River Text= 0 
```

河道名需用空格填充至固定宽度。

### 断面数据

```
Type RM Length L Ch R = 1 ,桩号,下游距离,下游距离,下游距离
Node Last Edited Time=Mon/DD/YYYY HH:MM:SS
#Sta/Elev= 测点数
       起点距1 高程1 起点距2 高程2 起点距3 高程3 ...
#Mann= 3 ,0,0
      左岸sta .nnn       0       0左岸sta .nnn       0  右岸sta .nnn       0
Bank Sta=左岸,右岸
XS Rating Curve= 0 ,0
XS HTab Starting El and Incr=最低高程,增距, 20
XS HTab Horizontal Distribution= 5 , 5 , 5
Exp/Cntr=0.3,0.1
```

⚠️ **关键格式要求**：
- `#Sta/Elev` 数据使用 **固定8字符列宽**（FORTRAN格式），每行10个值，而非空格分隔
- Manning's n 一行有9个值，每值8字符宽
- 不要有 `XS GIS Cut Line`（新版已不需要）
- 不要有 `BEGIN DESCRIPTION:`（新版用 `Geom Title=`）

### 流量文件 (.f01)

```
# # # # # STEADY FLOW DATA # # # # #

Number of Profiles=1
Profile Names=Q10

Flow Data in Reach
河道名 河道名
  桩号1  流量
  桩号2  流量
  ...

Boundary Conditions for Profiles
Profile 1: Q10
  最下游桩号  Known WS  水位值
  最上游桩号  Normal Depth  底坡
```

### 方案文件 (.p01)

```
Plan Title=方案名
Short Identifier=标识(≤24字符)
Program Version=7.00
Geometry File=g01
Flow File=f01
Plan ID=01
Flow Regime=2           # 0=亚临界 1=超临界 2=混合(Mixed)
Critical Depth Tolerance=0.01
Maximum Iterations=20
Calculation Tolerance=0.01
```

### 项目文件 (.prj)

```
Proj Title=项目名称
Default Exp/Contr=0.3,0.1
SI Units
Geom File=g01
Y Axis Title=Elevation
X Axis Title(PF)=Main Channel Distance
X Axis Title(XS)=Station
BEGIN DESCRIPTION:
  描述文字
END DESCRIPTION:
```

## HEC-RAS 批处理运行的限制

| 方法 | 可行性 | 说明 |
|:----|:------:|------|
| `ras.exe 项目.prj` | ❌ | 打开后挂起，需GUI操作 |
| `Steady.exe` | ❌ | 需要GUI触发 |
| `RasProcess.exe` | ⚠️ | 命令语法不明，文档极少 |
| COM接口 `RAS.RASProject` | ⚠️ | HEC-RAS 6+可用，需注册 |
| `Ras.exe /b` | ❌ | 无效参数 |
| **RAS Controller** | ✅ | HEC-RAS 5+提供COM控制接口，需regsvr32注册 `RAS.dll` |

**结论**：HEC-RAS 本质是 GUI 软件。批处理需要自己写程序调用 COM 接口，或直接生成 `.g01.hdf` 等预处理文件。

## 读取 DWG 图纸的工具链

DWG 是 Autodesk 私有二进制格式，需要用专业工具读取。

### 推荐方案：ezdxf + ODA File Converter

```bash
# 1. 安装 ODA File Converter（免费，winget 或官网下载）
winget install ODA.ODAFileConverter

# 2. 安装 Python ezdxf 库
pip install ezdxf

# 3. Python 读取 DWG
```

```python
from ezdxf.addons import odafc
import os

# 设置 ODA 转换器路径
os.environ['PATH'] += os.pathsep + r'C:\Program Files\ODA\ODAFileConverter 版本号'
odafc.converter_path = r'C:\Program Files\ODA\ODAFileConverter 版本号\ODAFileConverter.exe'

doc = odafc.readfile('图纸.dwg')
msp = doc.modelspace()
print(f'DWG版本: {doc.dxfversion}, 实体数: {len(msp)}')

# 遍历实体
for e in msp:
    print(f'图层:{e.dxf.layer} 类型:{e.dxftype()}')
```

### 从 CAD 提取断面间距（DMX 图层）

```
原理：CAD 中每条 DMX 线代表一个测流断面位置。
间距 = 相邻两条 DMX 线中点的直线距离。
```

```python
# 提取 DMX LINE 实体
dmx_lines = []
for e in msp:
    if e.dxf.layer == 'dmx' and e.dxftype() == 'LINE':
        s, e2 = e.dxf.start, e.dxf.end
        mx, my = (s.x+e2.x)/2, (s.y+e2.y)/2
        dmx_lines.append({'mx': mx, 'my': my})

# 按流向排序（Y坐标增/减方向）
dmx_lines.sort(key=lambda d: d['my'])
# 计算间距
for i in range(len(dmx_lines)-1):
    d = math.sqrt((dmx_lines[i+1]['mx']-dmx_lines[i]['mx'])**2 + 
                  (dmx_lines[i+1]['my']-dmx_lines[i]['my'])**2)
```

**替代工具**：

| 工具 | 费用 | 说明 |
|:----|:----|:-----|
| ODA File Converter | 免费 | 官方推荐，需要注册下载 |
| LibreDWG | 免费(GPL) | `dwg2dxf.exe` 命令行转换 |
| Aspose.CAD for Python | 付费 | 商业库，可直接读 DWG |
| AutoCAD + `pyautocad` | 付费 | 需安装 AutoCAD |
| LibreCAD | 免费 | 开源 CAD 编辑器，可打开 DWG 查看 |

## 陡坡水面线计算的注意事项

**核心问题**：能量方程在陡坡上有两个解（缓流 Fr<1 和急流 Fr>1），简单迭代易收敛到错误的浅水解。

### 症状

```
计算水位 vs HEC-RAS 结果偏差 > 2m
各断面水深突然跳到 0.1m（迭代下限）
Fr >> 1, 流速异常大（>100 m/s）
```

### 原因

```
E = z + h + V²/(2g)   →   同一个E值对应两个h
  解A (缓流): h=2.0m, V=0.4m/s,  Fr=0.09  ← 正确解
  解B (急流): h=0.1m, V=100m/s+, Fr>>1   ← 求解器常收敛至此
```

### 解决办法

1. **加 Fr < 1 约束**：搜索时跳过 Fr > 0.95 的解
2. **从深水向下搜索**：从 h=5m 开始往小搜，而非从 h=0.1m 往大搜
3. **计算临界水深 hc**：约束 h > hc
4. **分段处理**：急流段从上游往下游算，缓流段从下游往上游算，水跃处连接
5. **最根本方案**：使用 HEC-RAS Mixed Flow 模式

### 简化方案（陡坡山洪沟）

对于平均底坡 > 0.02 的山洪沟，可以分段用正常水深法近似：

```python
def calc_normal_depth(x_pts, z_pts, Q, n, i_local):
    """曼宁公式迭代求正常水深（适应陡坡）"""
    h = 0.3  # 初值
    for _ in range(50):
        A, P = 0, 0
        wl = min(z_pts) + h
        for j in range(len(x_pts)-1):
            if wl > z_pts[j] or wl > z_pts[j+1]:
                h1 = max(0, wl-z_pts[j])
                h2 = max(0, wl-z_pts[j+1])
                A += (h1+h2)/2*(x_pts[j+1]-x_pts[j])
                P += math.sqrt((x_pts[j+1]-x_pts[j])**2 + (z_pts[j+1]-z_pts[j])**2)
        if A > 0 and P > 0:
            R = A/P
            Q_c = 1/n * A * R**(2/3) * math.sqrt(max(i_local, 0.0001))
            if abs(Q_c - Q) < 0.01: break
            h *= Q / max(Q_c, 0.001)
            h = max(0.05, h)
        else: h += 0.1
    return h
```

## 水面线计算三步工作流

```
┌─────────────────────────────────────────────────────────┐
│  ① P-III 频率分析 → 设计洪峰 Qp                          │
│     输入：实测年最大流量系列                                │
│     方法：矩法初估 → 目估适线（规范规定方法）               │
│     输出：各频率设计洪峰 Q₁%/Q₂%/Q₅%...                   │
│     工具：Python scipy.stats.gamma / Excel                │
├─────────────────────────────────────────────────────────┤
│  ② 推理公式法 / 单位线法 → 设计洪水过程线 Q(t)            │
│     输入：流域面积F、主河长L、河道比降J、下垫面参数         │
│     方法：Qm = 0.278·ψ·S·F/τⁿ（迭代求解）               │
│     输出：各频率洪峰流量 + 洪水过程线                       │
│     工具：各省暴雨洪水查算手册软件 / Python                 │
├─────────────────────────────────────────────────────────┤
│  ③ 水面线计算 → 各断面设计洪水位 Zp                       │
│     输入：河道横断面、糙率n、设计流量Qp、边界水位           │
│     方法：标准步推法（HEC-RAS）/ 能量方程（Python）        │
│     输出：各断面水位、水深、流速                           │
│     工具：HEC-RAS / Python standard_step_method()         │
└─────────────────────────────────────────────────────────┘
```

> **⚠️ 数据准备占比 70%+**：水面线计算的实际工作量主要是断面数据的采集和整理。软件操作本身只占 30%。花时间把断面数据做准确，比追求软件功能更重要。
