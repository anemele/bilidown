# 哔哩哔哩用户投稿查询下载

移动互联网的发展衍生出封闭的网络生态，各大互联网逐渐限制对自家平台内容的访问。

为方便个人需求（自动下载某 up 的投稿），参考开源社区的成果，开发本项目。

本项目主要分为 3 个模块：

- 登录认证
- 交互操作
- 后台下载

**登录认证**

采用扫描二维码登录方式。
参考：<https://socialsisteryi.github.io/bilibili-API-collect/docs/login/login_action/QR.html#web%E7%AB%AF%E6%89%AB%E7%A0%81%E7%99%BB%E5%BD%95>

WBI 参考：<https://socialsisteryi.github.io/bilibili-API-collect/docs/misc/sign/wbi.html>

**交互操作**

用户投稿查询参考：<https://socialsisteryi.github.io/bilibili-API-collect/docs/user/space.html#%E6%8A%95%E7%A8%BF>

**后台下载**

本质上是网络爬虫，需要细心设计，防止触发反爬机制。
