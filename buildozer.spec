[app]
title = Jarvis AI
package.name = jarvisai
package.domain = org.assistant
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.1,plyer,requests
orientation = portrait
fullscreen = 1
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, CALL_PHONE, SEND_SMS, READ_CONTACTS, CAMERA, FLASHLIGHT
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
