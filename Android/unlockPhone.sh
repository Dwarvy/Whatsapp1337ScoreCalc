#!/bin/bash

#unlock device
adb shell input keyevent KEYCODE_WAKEUP;
adb shell input swipe 250 900 250 0 100;
