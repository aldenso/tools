#!/usr/bin/env python
# you need progressbar33: pip install progressbar33
import time
from progressbar import ProgressBar, AdaptiveETA, Bar, Percentage


def createprogress(count):
    """Return progress Bar"""
    widgets = [Percentage(),
               ' ', Bar(),
               ' ', AdaptiveETA()]
    pbar = ProgressBar(widgets=widgets, maxval=count)
    pbar.start()
    return pbar


def main():
    initial = 0
    items = [x for x in range(0, 10)]
    probar = createprogress(len(items))
    for _ in items:
        time.sleep(1)
        initial += 1
        probar.update(initial)
    probar.finish()


if __name__ == "__main__":
    main()
