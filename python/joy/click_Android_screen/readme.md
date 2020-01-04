#自动点击安卓手机屏幕某个区域,参考https://github.com/wangshub/wechat_jump_game

##step1，安装adb工具，搜索安装

##step2,用 ADB 工具获取当前手机截图，并用 ADB 将截图 pull 上来

adb shell screencap -p /sdcard/autojump.png

adb pull /sdcard/autojump.png .

##step3,安装mtpaint，方便查看像素坐标

##step4, ADB 工具点击屏幕蓄力一跳

adb shell input swipe x y x y time(ms)

