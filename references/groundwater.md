# 地下水时间序列分析（pastas）

> **依赖**：`pastas>=1.0.0, pandas, scipy` | **标签**：Groundwater, Time Series, Transfer Function
> **适用**：井水位对降水/抽水响应建模、含水层参数率定、水位预测/回推、水文信号分解
> **不适用**：三维地下水流（改用 FloPy+MODFLOW）、抽水试验分析（改用 Aqtesolv）

**核心类**：

| 类 | 用途 |
|------|------|
| `ps.Model` | 主模型容器 |
| `ps.StressModel` | 外部应力（抽水/河流）响应 |
| `ps.RechargeModel` | 降水-蒸发补给 |
| `ps.Gamma` | Gamma 分布响应函数 |
| `ps.Exponential` | 简单指数响应函数 |

**快速流程**：
```python
import pastas as ps
ml = ps.Model(head, name='Well_001')
sm = ps.RechargeModel(precip, evap, rfunc=ps.Gamma(), name='recharge')
ml.add_stressmodel(sm)
ml.solve()
ml.plot()
```

**诊断指标**：EVP > 70%（解释方差比）| RMSE | AIC/BIC（模型选择，越小越好）| 残差自相关检查

**常用模式**：
- 对比响应函数：Gamma vs Exponential vs Hantush → 用 AIC 选最优
- 应力分解：`ml.get_contributions()` 分离降水/抽水/趋势各自贡献
- 预测：`ml.simulate(tmin='2025-01-01', tmax='2026-12-31')`
- 保存/加载：`ml.to_json('model.pas')` / `ps.io.load('model.pas')`

**常见问题**：
| 问题 | 对策 |
|------|------|
| EVP 低 | 尝试不同响应函数 |
| 残差自相关 | `ml.solve(noise=True)` |
| 参数不稳定 | 设定参数边界或固定值 |
| 缺少应力数据 | 插值或建模前 `fillna()` |
