openclaw-addons
================

一个为 OpenClaw 精选的插件、技能与工具集合。

本仓库当前包含两个示例技能：

- **邮箱发送技能（Email skill）**：通过常见的国内外邮箱服务提供商发送邮件，例如 Gmail、QQ 邮箱、163 邮箱，以及其他任何支持 SMTP 的邮箱。
- **阿里云短信技能（Aliyun SMS skill）**：通过阿里云短信服务发送短信验证码或通知类短信。

> 说明：本项目使用 Python 实现技能逻辑，OpenClaw 可以通过子进程或作为库调用这些技能。

### 项目结构

- `skills/email_sender`：邮箱发送技能（基于 SMTP，可连 Gmail/QQ/163 等）。
- `skills/aliyun_sms`：阿里云短信发送技能。
- `requirements.txt`：上述技能所需的 Python 依赖。

### 运行前提

- **Python 版本**：建议 3.9 及以上。
- **依赖安装**：使用下面命令安装：

```bash
pip install -r requirements.txt
```

- **网络连通性**：运行 OpenClaw 的环境需要能访问：
  - 各邮件服务商的 SMTP 服务（如 Gmail、QQ、163 等）。
  - 阿里云短信服务的 API 端点。

---

## 邮箱发送技能（`skills/email_sender`）

该技能基于 Python 标准库 `smtplib` 实现，通过读取 stdin 中的 JSON 请求来发送邮件，并在 stdout 上输出 JSON 格式的结果。OpenClaw 可以将其当作一个通用的“发送邮件”工具。

### 支持的典型邮箱服务商（示例）

- **Gmail**：`smtp.gmail.com:587`（TLS）
- **QQ 邮箱**：`smtp.qq.com:465`（SSL）或 `smtp.qq.com:587`（TLS）
- **163 邮箱**：`smtp.163.com:465`（SSL）或 `smtp.163.com:25/587`（TLS）

> 你也可以为其他支持 SMTP 的邮箱服务配置对应的 `smtp_host` 和 `smtp_port`。

### 环境变量（可选）

- `EMAIL_DEFAULT_FROM`：默认发件地址（当请求中未指定 `from_addr` 时使用）。

### 请求格式（stdin JSON）

```json
{
  "smtp_host": "smtp.qq.com",
  "smtp_port": 465,
  "use_ssl": true,
  "username": "your_account@qq.com",
  "password": "your_smtp_or_app_password",
  "from_addr": "your_account@qq.com",
  "to_addrs": ["target@example.com"],
  "subject": "Hello from OpenClaw",
  "body": "This is a test email from the OpenClaw email skill.",
  "body_type": "plain"
}
```

### 返回格式（stdout JSON，示例）

```json
{
  "ok": true,
  "message_id": "smtp-message-id-or-empty",
  "error": null
}
```

当发送失败时，`ok` 为 `false`，`error` 字段会包含错误说明。

---

## 阿里云短信技能（`skills/aliyun_sms`）

该技能使用阿里云官方 Python SDK（`alibabacloud_dysmsapi20170525` 等），用于向指定手机号发送短信。

### 环境变量

在运行前，请配置以下环境变量（或在你的调用层负责传入这些配置）：

- `ALIYUN_ACCESS_KEY_ID`：阿里云 AccessKey ID
- `ALIYUN_ACCESS_KEY_SECRET`：阿里云 AccessKey Secret
- `ALIYUN_REGION_ID`：地域 ID，例如 `cn-hangzhou`
- `ALIYUN_SMS_SIGN_NAME`：短信签名
- `ALIYUN_SMS_TEMPLATE_CODE`：短信模板编码

### 请求格式（stdin JSON）

```json
{
  "phone_numbers": ["13800000000"],
  "template_params": {
    "code": "123456"
  }
}
```

- `phone_numbers`：要发送的手机号数组（会在内部拼接为逗号分隔）。
- `template_params`：模板变量，最终会转成 JSON 字符串传给阿里云短信模板。

### 返回格式（stdout JSON，示例）

```json
{
  "ok": true,
  "request_id": "ABCDEF123456",
  "biz_id": "1234567890",
  "error": null
}
```

当发送失败时，`ok` 为 `false`，`error` 字段会包含阿里云返回的错误码与信息。

---

## 与 OpenClaw 集成的思路

- 通过 **子进程调用**：OpenClaw 将请求体（JSON）写入对应技能脚本的 stdin，然后读取 stdout 的 JSON 结果。
- 通过 **Python 模块调用**：也可以在 OpenClaw 的运行时直接 `import skills.email_sender` / `skills.aliyun_sms`，调用其导出的函数。

根据你的 OpenClaw 集成方式，可以自由封装一层适配器。

