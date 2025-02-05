[app]

# 应用信息
title = Collision Demo
package.name = collision_demo
package.domain = org.example
source.dir = .

# 主程序入口
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
requirements = python3,pygame,kivy

# Android 配置
android.accept_sdk_license = True
android.ndk = 25b
android.sdk = 26
android.archs = arm64-v8a

# 权限配置
android.permissions = INTERNET

# 图标配置（需要准备图标文件）
# icon.filename = %(source.dir)s/icon.png

# 屏幕方向
orientation = landscape

# 调试模式
log_level = 2
