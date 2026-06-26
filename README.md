# water-engineering — 水利工程领域专用 Claude Code Skill

[![Skill](https://img.shields.io/badge/Claude_Code-Skill-8A2BE2)](https://code.claude.com)
[![Version](https://img.shields.io/github/v/release/WhOleit-hub/water-engineering-skill)](https://github.com/WhOleit-hub/water-engineering-skill/releases)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

一套完整的**水利水电工程领域 AI 辅助设计技能**，为中国水利工程师打造，覆盖水文计算、水工设计、中国标准规范、施工组织、工程经济等全专业领域。

---

## 核心能力

| 模块 | 内容 |
|------|------|
| **标准规范** | 国标 12 部 + 水利行标 50+ 部（含 2024-2026 最新发布） |
| **水文计算** | P-III 频率曲线、设计洪水、暴雨推求、马斯京根法、水库兴利调节、PMF |
| **水力学** | 明渠流、水面线计算、水跃、堰流（WES/宽顶堰）、消能、渗流 |
| **水工建筑物** | 重力坝、土石坝、水闸、溢洪道、水工隧洞 |
| **水工结构** | 水工钢筋混凝土（SL 191/DL/T 5057）、水工钢结构、挡土墙 |
| **水电站** | 引水系统、水锤调保、水轮机选型、厂房布置 |
| **灌溉排水** | 灌溉原理、灌水方法、渠道设计、排水系统 |
| **河流动力学** | 泥沙运动、河床演变、河道整治 |
| **地下水** | 传递函数噪声模型、含水层参数率定（整合 pastas 技能） |
| **计算软件** | 远盛水工、理正岩土、理正结构工具箱、AutoBank、HEC-RAS、MIKE 11 |
| **报告模板** | 可研/初设/防洪评价/水文专题/水资源论证/大坝安全评价/山洪沟治理标准目录 |
| **批复文书** | 水利部 22 种水行政许可文书模板 |
| **实战项目库** | 40+ 个福建水利工程项目（2023-2026）经验数据 |

---

## 版本与迭代

| 版本 | 日期 | 说明 |
|:----:|:----:|:----|
| v1.0.0 | 2026-06-26 | 首次发布，行数优化 2322→1027（-56%） |

开发在 `develop` 分支进行，稳定后合并到 `master` 并发布 Release。

---

## 安装使用

```bash
# 克隆到 Claude Code skills 目录
git clone https://github.com/WhOleit-hub/water-engineering-skill.git ~/.claude/skills/water-engineering

# 在 Claude Code 中调用
/water-engineering
```

---

## 文件结构

```
water-engineering/
├── skill.md                  # 主技能文件（1027行）
├── CHANGELOG.md              # 版本变更记录
├── VERSION                   # 当前版本号
├── Makefile                  # 发布命令
├── README.md                 # 本文件
└── references/
    ├── report-templates.md       # 报告目录+批复文书（531行）
    ├── structural-engineering.md # 钢筋砼+钢结构（140行）
    ├── hydropower-irrigation.md  # 水电站+灌溉+河流动力学（136行）
    ├── software.md               # 计算软件操作指南（361行）
    ├── external-tools.md         # HEC-RAS/MIKE 11/Python引擎（893行）
    ├── projects.md               # 实战工程经验库（190行）
    ├── groundwater.md            # 地下水时间序列分析
    ├── landlab.md                # 地表过程与河流地貌建模
    └── external-tools.md         # HEC-RAS/MIKE 11/Python水面线引擎
```

---

## 适用场景

- 📐 **水利工程设计** — 可研/初设报告编写，提供标准章节模板
- 🌊 **水文分析与计算** — P-III 频率分析、设计洪水推求
- 🏗️ **水工结构计算** — 挡土墙、水闸、重力坝、土石坝
- 📝 **行政许可申请** — 防洪评价、水资源论证报告编制
- 🖥️ **软件操作指导** — 远盛水工、理正岩土、HEC-RAS 等

---

## 贡献

欢迎水利同行贡献：
1. Fork 本仓库
2. 在 `develop` 分支提交更改
3. 发起 Pull Request 到 `develop`
4. 稳定后合并到 `master`，发布新版本

---

## 许可

MIT License
