# GLaDOS Auto Checkin

> GitHub Actions 实现 GLaDOS 自动签到 —— 零成本、零依赖、零维护，每天自动签到，账号天数稳稳续上。

[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Runs on](https://img.shields.io/badge/Runs%20on-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Notification](https://img.shields.io/badge/Notification-PushPlus-2088FF)](https://www.pushplus.plus/)

> [!IMPORTANT]
> **注册 GLaDOS 可用邀请码：`6QKWG-GO5N3-P97RU-77RHK`，双方都有奖励天数**

[GLaDOS](https://glados.cloud) 账号每天签到能持续累积天数，手动签到费时费力还容易忘。
本项目利用 GitHub Actions 的免费定时任务帮你自动完成签到，并把签到结果推送到你的微信。

## 邀请福利

还没有 GLaDOS 账号？注册时填写下面的邀请码，**你和作者都会获得奖励天数**：

```
6QKWG-GO5N3-P97RU-77RHK
```

## 特性

| 特性     | 说明                                             |
| -------- | ------------------------------------------------ |
| 零成本   | 运行在 GitHub Actions 免费额度上，无需任何服务器 |
| 零依赖   | 纯 Node.js 内置 `fetch`，脚本本身零第三方依赖    |
| 自动签到 | 每天定时调用官方签到接口，自动续期               |
| 状态查询 | 签到后自动查询并展示剩余天数                     |
| 失败告警 | Cookie 过期、签到异常时第一时间推送提醒          |
| 微信通知 | 通过 PushPlus 推送签到结果到微信（可选）         |

## 快速开始

只需 4 步，5 分钟完成部署。

### 第 1 步：Fork 本仓库

点击右上角 **Fork**，将本仓库 Fork 到你自己的账号下。

### 第 2 步：获取 GLaDOS Cookie

1. 登录 [glados.cloud](https://glados.cloud)
2. 打开浏览器开发者工具（`F12` 或 `Cmd + Option + I`）
3. 切换到 **Network（网络）** 标签，刷新页面
4. 点击任意一个请求，在 **Request Headers** 中找到 `cookie` 字段，复制完整值

Cookie 形如：

```
koa:sess=xxxxxx; koa:sess.sig=xxxxxx
```

### 第 3 步：配置 Secrets

在你的 Fork 仓库中，进入 **Settings → Secrets and variables → Actions → New repository secret**，添加：

| Secret 名称 | 必填 | 说明                                                         |
| ----------- | ---- | ------------------------------------------------------------ |
| `GLADOS`    | 是   | 第 2 步复制的完整 Cookie                                     |
| `NOTIFY`    | 否   | [PushPlus](https://www.pushplus.plus/) 的 Token，用于微信推送签到结果 |

Cookie 通过 GitHub Secrets 加密存储，不会出现在代码和运行日志中。

### 第 4 步：启用 Actions

本仓库已内置 `.github/workflows/run.yml`，Fork 后自动携带，无需手动创建：

```yaml
name: run

on:
  workflow_dispatch:
  push:
  schedule:
    - cron: '0 2 * * *'

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run main
        env:
          GLADOS: ${{ secrets.GLADOS }}
          NOTIFY: ${{ secrets.NOTIFY }}
```

默认每天北京时间 10:00（UTC 02:00）执行，如需调整时间，修改 `cron` 表达式即可。除定时执行外，push 代码和手动触发也会运行一次签到。

Fork 后进入仓库的 **Actions** 页面，点击 **I understand my workflows, go ahead and enable them** 启用定时任务，再手动 Run 一次验证配置，之后每天自动执行。

## 运行效果

签到成功时，控制台与微信推送会收到：

```
[ 'Checkin OK', 'Checkin! Got 8 points', 'Left Days 427' ]
```

Cookie 过期或签到异常时，会收到告警，提醒你及时更新 Secrets：

```
[
  'Checkin Failed',
  '...',
  'Cookie 可能已过期,请重新登录后更新 GitHub Secrets 的 GLADOS',
  '<你的仓库链接>'
]
```

## 常见问题

**Q: 签到失败，提示 Cookie 可能已过期？**
Cookie 有一定有效期（通常约 1 个月），重新登录 [glados.cloud](https://glados.cloud)，按第 2 步获取新 Cookie，更新 `GLADOS` Secret 即可。

**Q: 定时任务没有准点执行？**
GitHub Actions 的 `schedule` 存在几分钟到几十分钟的排队延迟，属正常现象，不影响签到。

**Q: 如何手动触发一次签到？**
Actions → run → Run workflow。

**Q: 支持多账号吗？**
当前版本支持单账号。多账号可 Fork 多份，或自行改造为 matrix 多任务。

## 工作原理

```
GitHub Actions 定时触发
          |
          v
    glodos_git.js
          |
          +--> POST /api/user/checkin    每日签到
          +--> GET  /api/user/status     查询剩余天数
          |
          +--> 签到失败 / Cookie 过期 --> 告警推送
          +--> 签到成功                --> PushPlus 微信推送
```

## 免责声明

- 本项目仅供个人学习与自动化使用，请遵守 GLaDOS 服务条款
- Cookie 属于敏感信息，请勿泄露给他人

## License

[MIT](LICENSE)

---

如果这个项目帮到了你，欢迎点一个 **Star**，这是对作者最大的鼓励。
