# 贡献指南

感谢你对 Claude Skills 项目的兴趣！

## 如何贡献

### 提交 Bug 报告

在提交新的 Issue 之前，请先搜索现有的 Issues，看看是否已经有人报告了同样的问题。

### 添加新 Skill

1. 在 `claude_skills/` 目录下创建新的子目录
2. 创建以下文件：
   - `__init__.py` - 模块初始化
   - `<skill_name>.py` - 主要实现
   - `SKILL.md` - Skill 定义文档
   - `README.md` - 详细说明
   - `example.py` - 使用示例
   - `requirements.txt` - 依赖列表
3. 在根目录的 `requirements.txt` 中添加新的依赖
4. 更新根目录的 `README.md`，添加新 Skill 的说明
5. 在 `claude_skills/__init__.py` 中导出新 Skill

### 开发流程

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 代码规范

- 遵循 PEP 8 风格
- 使用有意义的变量和函数名
- 为公共 API 添加文档字符串
- 保持代码简洁和可读性

## 运行测试

```bash
pip install -e ".[dev]"
pytest
```

## 许可证

通过贡献代码，你同意你的贡献将根据项目的 MIT 许可证进行许可。
