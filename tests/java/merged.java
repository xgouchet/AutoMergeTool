package com.deezer.core.data.common.util;

import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
<<<<<<< LOCAL

import android.media.AudioManager;
|||||||
import android.action.Foo;
=======

import android.annotation.SuppressLint;
import android.content.Context;
import android.media.PlaybackParams;
import android.os.Build;
import android.os.HandlerThread;
>>>>>>> REMOTE
import android.os.Looper;

import org.greenrobot.eventbus.EventBus;

<<<<<<< LOCAL
import java.lang.String;
|||||||
import android.action.Foo;
=======
import java.lang.Integer;
>>>>>>> REMOTE
import java.util.Locale;

public class Test {

    int i;
    float f;
    short s;

    public Test(){
<<<<<<< LOCAL
        i = 42;
        f = 3.1416f;
        s = 2;
|||||||
        i = 42;
        f = 3.14f;
        s = 2;
=======
        i = 421;
        f = 3.14f;
        s = 12;
>>>>>>> REMOTE
    }

<<<<<<< LOCAL
    void foo() {
    }
|||||||
=======
    public boolean bar (int j) {
        return i%j == 0;
    }
>>>>>>> REMOTE

}
