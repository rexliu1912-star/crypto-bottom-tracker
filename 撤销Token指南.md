# 🔐 撤销泄露的 Telegram Bot Token - 操作指南

## ⚠️ 重要：必须立即撤销旧 Token

旧的 Token `8572033784:AAGGdNMW-lxnMJq5MuGld-uDbAX8AoeEUfs` 已经在 GitHub 上公开，**任何人都可以使用它**。

## 📱 操作步骤（5分钟）

### 1. 打开 Telegram

在手机或电脑上打开 Telegram

### 2. 找到 BotFather

- 在搜索框中输入 `@BotFather`
- 点击官方的 BotFather（带蓝色验证标志）
- 或直接点击：https://t.me/BotFather

### 3. 查看你的 Bots

发送命令：
```
/mybots
```

BotFather 会列出你所有的 Bots

### 4. 选择你的 Bot

点击你用于这个项目的 Bot 名称

### 5. 进入 API Token 设置

点击 `API Token` 按钮

### 6. 撤销旧 Token ⚠️

1. 点击 `Revoke current token`
2. 确认撤销（这会使旧 Token 立即失效）
3. ✅ 旧 Token 现在已无法使用

### 7. 生成新 Token ✨

1. 点击 `Generate new token`
2. BotFather 会返回新的 Token，格式类似：
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
   ```
3. **重要：立即复制这个新 Token**
4. 不要关闭对话，保持 Telegram 打开

---

## ✅ 完成后的检查清单

- [ ] 我已经撤销了旧 Token
- [ ] 我已经生成了新 Token
- [ ] 我已经复制了新 Token（准备粘贴到 .env 文件）

## 🔄 下一步

完成上述操作后，请：

1. 返回终端
2. 告诉我你已经获取了新 Token
3. 我会帮你更新配置并测试

---

## 💡 提示

- 生成新 Token 后，旧 Token 立即失效
- 新 Token 同样不要分享给任何人
- 不要在代码中硬编码新 Token
- 只在 `.env` 文件中保存（该文件不会被 Git 追踪）

## ❓ 如果遇到问题

- **找不到 BotFather？** 确保搜索时包含 `@` 符号
- **没有权限？** 确保你是 Bot 的创建者
- **Token 显示无效？** 检查是否完整复制（不要有多余空格）
