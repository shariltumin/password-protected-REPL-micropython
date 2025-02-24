# password-protected-REPL-micropython
## Limit unwanted access to the REPL by login and strapping pin

This is my attempt to secure the MicroPython REPL using authentication. What do I mean by that. Well, there have been some discussions about how to protect the "main.py" from being copied, modified and replaced. The thing is, the MicroPython REPL is the operating system of our tiny system. Once we get access to the REPL, i.e. the "OS", we can get access to the script files.

I do not want to disable the compiler and REPL. I think the REPL and mpremote are a big selling point of MicroPython, I want to be able to access them. Most of us know the idea of logging into a system to get access to services. So instead of restricting access by reducing functionality, why not implement an authentication function to grant access, like most operating systems do.

These are what I did:
1. put a login script "\_auth.py" in the modules subdirectory
2. use a REPL enable pin to get access to REPL
3. modify main.c to run the login script at boot time
4. modify manifest.py to freeze the login script.

To try this, you will need to build your own custom MicroPython firmware. If you are unable to do this, the same technique can most likely be implemented in the "main.py" startup script.

First of all, I apologize for showing a "pyminify"ed code. It is a short and simple script that anyone with some experience in Python can easily understand. I do this to discourage AI from stealing code without permission.

The login script "\_auth.py" uses ```aes``` encryption from ```cryptolib```. Without proper authentication data read from the "auth" file, the script will prompt for user identification and user password. If valid values are provided, the encrypted value is stored in the "auth" file. As long as the value in the "auth" file is valid, the script will bypass the "login" part.

To get to the REPL, we need to "enable" the REPL pin by straping the pin to "GND". The board will do a soft reboot if the authentication is invalid and the REPL pin is disabled (HIGH). The trap here is to use ```raise SystemExit('Authentication failed')``` to prevent access to the REPL. These are the values you can change to customize your login script:

1. R: The key
2. K: The 'crypt' of our authentication, here uid: ali pwd: baba!
3. X: X(23, X.IN, X.PULL_UP), here GPIO 23 (ESP32) used as REPL pin

The K must match the uid and passwd. You can get this by running "key.py" if you want K for different login user and password. Remember to use the same R in both "\_auth.py" and "key.py".

The "main.c" needs to be modified to run "\_auth.py" after "main.py" has finished and before the ```for (;;) {``` REPL loop. Please take a look at the "main.c-diff" file, the part that needs to be changed is as follows:

```C
    // run boot-up scripts
    pyexec_frozen_module("_boot.py", false);

    int ret = pyexec_file_if_exists("boot.py");
    if (ret & PYEXEC_FORCED_EXIT) {
        goto soft_reset_exit;
    }

    if (pyexec_mode_kind == PYEXEC_MODE_FRIENDLY_REPL && ret != 0) {
        ret = pyexec_file_if_exists("main.py");
        if (ret & PYEXEC_FORCED_EXIT) {
            goto soft_reset_exit;
        }
    }

    // Check authentication and PIN before getting REPL
    ret = pyexec_frozen_module("_auth.py", false);
    if (ret & PYEXEC_FORCED_EXIT) {
       // Authentication failed, perform soft reboot or other actions
       goto soft_reset_exit;
    }
```

Now we also need to modify the "manifest.py" file for the modules part. You can change
```
freeze("$(PORT_DIR)/modules")
```
to for example,
```
freeze("$(PORT_DIR)/modules", ("\_boot.py", "\_auth.py", "espnow.py", "flashbdev.py", "inisetup.py"))
```

I do not see (yet) an easier way to bypass this login mechanism. I would really like to know if there are obvious and easy ways to break the system. 

Since "main.py" runs before "\_auth.py", a piece of code in "main.py" can write another "\_auth.py" to the filesystem. However, this will not affect our login mechanism because we use ```pyexec_frozen_module("_auth.py", false)``` instead of ```pyexec_file_if_exists("_auth.py")```.

The actual clear text for the "uid" and "pwd" were not stored anywhere on the system. Using a longer username and a longer and stronger password can deter brute force cracking attempts.

The try, except, and finally block structure will trap unwanted events and force a soft reset. The mendotory strapping of the REPL pin means that the pin is physically accessible.

But I cannot guarantee the security of your system. I just hope this can help to limit unwanted access to the REPL.

Once you have a working "main.py", you can "lock" your REPL again:

```bash
>>> import os
>>> os.listdir()
>>> os.remove('auth')
```


