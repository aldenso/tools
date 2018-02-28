# Catching signals

A way to exit a program when you type ctrl+c (KeyboardInterrupt) or get a kill (-15) signal.

```sh
python_examples/signals/catchsignal.py
```

Example when: ctrl+c

```txt
doing something
doing something
doing something
doing something
^Cterminating loop
```

example when: kill $PID

```txt
doing something
doing something
doing something
doing something
terminating loop
```
