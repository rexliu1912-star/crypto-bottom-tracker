# 🔒 Security Policy / 安全策略

## Reporting a Vulnerability / 报告漏洞

If you discover a security vulnerability, please report it by creating a private security advisory on GitHub.

如果您发现安全漏洞，请通过 GitHub 创建私有安全建议来报告。

## Security Best Practices / 安全最佳实践

### ⚠️ Never Commit Secrets / 永远不要提交密钥

**DO NOT** commit any of the following to the repository:
- API keys / API 密钥
- Tokens / 令牌
- Passwords / 密码
- Private keys / 私钥

**不要**将以下内容提交到仓库：
- API 密钥
- 令牌
- 密码
- 私钥

### ✅ Proper Configuration / 正确的配置方式

**Use Environment Variables (Recommended):**

1. Copy `.env.example` to `.env`
2. Fill in your actual secrets in `.env`
3. The `.env` file is already in `.gitignore` and will NOT be committed

**使用环境变量（推荐）：**

1. 复制 `.env.example` 为 `.env`
2. 在 `.env` 中填入你的真实密钥
3. `.env` 文件已在 `.gitignore` 中，不会被提交

**Example `.env` file:**
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=-1001234567890
POLYGON_API_KEY=your_actual_api_key_here
```

### 🔄 If You Accidentally Committed Secrets / 如果不小心提交了密钥

**Immediate Actions Required:**

1. **Revoke/Rotate the exposed secrets immediately**
   - Telegram: Use [@BotFather](https://t.me/BotFather) to revoke and regenerate token
   - Polygon.io: Log in and regenerate API key

2. **Remove secrets from Git history:**
   ```bash
   # Warning: This rewrites history and requires force push
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch crypto-bottom-tracker.py" \
   --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push to overwrite remote:**
   ```bash
   git push origin --force --all
   ```

**立即采取的行动：**

1. **立即撤销/重新生成暴露的密钥**
   - Telegram：使用 [@BotFather](https://t.me/BotFather) 撤销并重新生成令牌
   - Polygon.io：登录并重新生成 API 密钥

2. **从 Git 历史中删除密钥**（见上方命令）

3. **强制推送覆盖远程仓库**（见上方命令）

### 📋 Security Checklist / 安全检查清单

Before committing, always check:
- [ ] No hardcoded secrets in code
- [ ] `.env` file is in `.gitignore`
- [ ] Only `.env.example` is committed (with placeholder values)
- [ ] Run `git diff` to review changes
- [ ] Use `git secrets` or similar tools to scan for secrets

提交前，始终检查：
- [ ] 代码中没有硬编码的密钥
- [ ] `.env` 文件在 `.gitignore` 中
- [ ] 仅提交 `.env.example`（包含占位符值）
- [ ] 运行 `git diff` 检查更改
- [ ] 使用 `git secrets` 等工具扫描密钥

## Supported Versions / 支持的版本

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Contact / 联系方式

For security concerns, please create a private security advisory on GitHub.

如有安全问题，请在 GitHub 上创建私有安全建议。
