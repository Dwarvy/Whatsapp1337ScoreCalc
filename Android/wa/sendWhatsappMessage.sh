#!/bin/bash

#unlock device
adb shell input keyevent KEYCODE_WAKEUP;
adb shell input swipe 250 900 250 0 100;

#home device
adb shell input keyevent KEYCODE_HOME;
adb shell input keyevent KEYCODE_HOME;

#open whatsapp
adb shell input tap 353 290
#open first chat
adb shell input tap 232 187

#type text (dont send yet)
adb shell input text \"$1\";
#press enter (to send)
adb shell input keyevent KEYCODE_ENTER

#press back button a frew times to reset app to home screen
adb shell input keyevent KEYCODE_BACK
adb shell input keyevent KEYCODE_BACK
adb shell input keyevent KEYCODE_BACK

#Lock the screen
adb shell input keyevent 26
