package com.deezer.core.data.common.util;

import android.support.annotation.NonNull;
import android.support.annotation.Nullable;

import android.annotation.SuppressLint;
import android.content.Context;
import android.media.PlaybackParams;
import android.os.Build;
import android.os.HandlerThread;
import android.os.Looper;

import org.greenrobot.eventbus.EventBus;

import java.lang.Integer;
import java.util.Locale;

public class Test {

    int i;
    float f;
    short s;

    public Test(){
        i = 421;
        f = 3.14f;
        s = 12;
    }

    public boolean bar (int j) {
        return i%j == 0;
    }

}
