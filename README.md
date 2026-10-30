# OK-Script macOS

本项目基于 [ok-oldking/ok-script](https://github.com/ok-oldking/ok-script) 二次开发，为 [OK-WW macOS](https://github.com/Junsheng-He-Life/ok-wuthering-waves) 提供配套自动化框架。它是非官方 macOS 派生版本，保留上游作者与贡献者的归属及原始 [LICENSE.txt](LICENSE.txt)（GNU AGPL v3 文本）。

游戏任务来自基于 [原版 OK-WW](https://github.com/ok-oldking/ok-wuthering-waves) 修改的配套仓库；本框架不是游戏官方产品，也不是原作者发布的正式 macOS 版。

## 获取配套内测版

普通使用者请下载 [OK-WW v0.1.0-beta.1 配套包](https://github.com/Junsheng-He-Life/ok-wuthering-waves/releases/tag/v0.1.0-beta.1)，并阅读[安装与使用教程](https://github.com/Junsheng-He-Life/ok-wuthering-waves/blob/v0.1.0-beta.1/docs/beta-user-guide.md)。包中包含两个匹配项目、安装入口和固定依赖，无需安装 Codex。

- 安装条件：Apple Silicon Mac、macOS 14+、Python 3.13、Xcode Command Line Tools。
- 当前 Python 包版本为 `1.0.175+macos.1`，两个仓库的配套发布标签均为 `v0.1.0-beta.1`。
- Python 导入名保持为 `ok`。请使用配套本地源码，不要用 PyPI 上的另一版本替换。
- 此包为源码内测版，不是经过签名、公证或自带 Python 的 `.app`。

## macOS 后端的改动

- ScreenCaptureKit 窗口捕获与 Quartz 前台键鼠输入。
- Retina 像素与逻辑坐标转换、窗口标题栏处理及前台窗口选择。
- 记录窗口与显示器几何信息；游戏任务检测到变化后停止新输入，仍允许释放已按下的按键。
- 启动时保留实际分辨率错误；并发采集请求只保留一个活动流。
- 本地固定版本号构建，不通过网络推算软件包版本。

任务执行要求游戏位于前台。跨显示器、修改缩放及不同 macOS 版本上的完整游戏流程仍待实机验收，不承诺后台运行。

## 开发与验证

两个仓库放在同一个父目录，并检出同名标签。安装与公开测试命令见 [开发文档](https://github.com/Junsheng-He-Life/ok-wuthering-waves/blob/v0.1.0-beta.1/docs/development.md)。

本次框架公开离线子集有 **49 项通过**，排除 1 项原生权限探针；使用合成图像和模拟输入，不要求启动游戏。应用公开子集有 111 项通过。上述结果不代表真实硬件切屏或战斗验收。

框架 API 与原有平台背景可查阅 [上游文档](https://github.com/ok-oldking/ok-script/tree/master/docs)。Windows、模拟器与浏览器使用者优先参考上游对应版本，本 fork 的 macOS 发行说明不作为其他平台的验证承诺。

## 反馈与归属

框架问题提交至 [本仓库 Issues](https://github.com/Junsheng-He-Life/ok-script/issues)，游戏任务或面板问题提交至 [OK-WW macOS Issues](https://github.com/Junsheng-He-Life/ok-wuthering-waves/issues)。附上配套标签、Mac/系统信息和脱敏的复现步骤。

感谢 [OK-Script](https://github.com/ok-oldking/ok-script) 与 [OK-WW](https://github.com/ok-oldking/ok-wuthering-waves) 原作者和贡献者。原有源码版权声明继续保留，第三方依赖遵循各自许可。
