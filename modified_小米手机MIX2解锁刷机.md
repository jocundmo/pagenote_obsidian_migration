---
date: 2022-11-19 19:25:41
tags: [刷机, xiaomi]
---

* 先要BL解锁，安装解锁工具 miflash_unlock-6.5.406.31
* 按照提示操作，具体参考[此文](https://miuiver.com/how-to-unlock-xiaomi-phone/)
* 解锁碰到的第一个问题就是插上手机后没反应，即使显示成功安装了驱动也没用
	* 解决方案在[这里](https://zhuanlan.zhihu.com/p/216568708)  [本地知识库](file:///D:/Clips_migration_testing/百科/数码/小米手机解锁工具出现不提示连接等问题的解决方法_12bfc532b948a9272ab2c738c30be27a3ced2165.html)
* 能成功认出手机后碰到第二个问题是50%进度时没有反应，无奈等了半个小时后只能关掉重新来，这次倒是成功了，不过报错“解锁失败，参数错误”
* 经网上查询需要打开手机，进入开发者模式，查询“设备解锁状态”，然后点击“绑定账号和设备”
	* 又碰到问题“验证失败，请重新登录您的账号再次尝试”，退出小米账号后重新登录即可
	* 解锁成功
* 打开MiFlash2020-3-14-0，选中线刷包(只要选目录即可)，手机fastboot模式启动(音量下+电源键) 参考[此文](https://miuiver.com/how-to-flash-xiaomi-phone/)
	* 一定要选“全部删除”模式
	* 结果又碰到error: Not catch checkpoint问题，经查[这里](https://miuiver.com/miflash-error-not-catch-checkpoint/)说不是问题
	* 也可选择菜单Configuration中，将Ch
* 点加载设备，再点刷机即可
* 最终一定要等到刷机结果显示“success”，即使手机开机了也不要去操作

最后结果可参考此贴
[本地知识库](file:///D:/Clips_migration_testing/百科/数码/小米手机解锁及线刷教程_167d24a570d126e5b5182c7f805dda7d54e814e1.html)
