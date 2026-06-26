# 地表过程与河流地貌建模（Landlab）

> **依赖**：`landlab>=2.6.0, numpy, matplotlib` | **标签**：Landscape Evolution, Geomorphology, Erosion, Flow Routing
> **适用**：景观演化模拟/河流侵蚀/水流路由/坡面扩散/风化土壤生成/排水网络分析
> **不适用**：盆地尺度地层学（改用 Badlands）、简单扩散侵蚀（改用自定义 numpy）

**网格类型**：

| 网格 | 用途 |
|------|------|
| `RasterModelGrid` | 规则矩形网格（最常用） |
| `HexModelGrid` | 六边形网格（各向同性流） |
| `VoronoiDelaunayGrid` | 不规则点分布 |
| `NetworkModelGrid` | 仅河道网络 |

**快速流程**：
```python
from landlab import RasterModelGrid
from landlab.components import FlowAccumulator, StreamPowerEroder, LinearDiffuser

grid = RasterModelGrid((100, 100), xy_spacing=100.0)
z = grid.add_zeros('topographic__elevation', at='node')
z += np.random.rand(grid.number_of_nodes) * 0.1
grid.set_closed_boundaries_at_grid_edges(True, True, True, False)

fa = FlowAccumulator(grid, flow_director='D8')
sp = StreamPowerEroder(grid, K_sp=1e-5)
ld = LinearDiffuser(grid, linear_diffusivity=0.01)

for _ in range(500):
    fa.run_one_step()
    sp.run_one_step(dt=1000)
    ld.run_one_step(dt=1000)
    z[grid.core_nodes] += 0.001 * 1000  # uplift
```

**核心组件**：`FlowAccumulator`（D8/Steepest/MFD 流向）| `StreamPowerEroder`（河流侵蚀 K_sp）| `LinearDiffuser`（坡面扩散）

**水利关联**：
- 流域地貌演化 → 理解河道形态成因
- 水流路由 → 与产汇流模型的 DEM 前处理互补
- 河道纵剖面提取 → 与河流动力学河道整治联动

**常见问题**：平坦区无流向→加微小随机噪声 | 边界效应→确保至少一侧开放 | 侵蚀不稳定→减小 dt 或 K_sp
