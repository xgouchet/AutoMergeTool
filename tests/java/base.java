package com.deezer.core.data.common.util;

import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.annotation.VisibleForTesting;

import android.annotation.SuppressLint;
import android.content.Context;
import android.os.HandlerThread;
import android.os.Looper;

import org.greenrobot.eventbus.EventBus;

import java.util.Locale;

public class Test {

    int i;
    float f;
    short s;

    public Test(){
        i = 42;
        f = 3.14f;
        s = 2;
    }
}
