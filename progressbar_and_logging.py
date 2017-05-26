#!/usr/bin/python
# @CreateTime: May 26, 2017 1:54 PM
# @Author: Aldo Sotolongo
# @Contact: aldenso@gmail.com
# @Last Modified By: Aldo Sotolongo
# @Last Modified Time: May 26, 2017 2:24 PM
# @Description: example progress bar operation with logging included

import time
import random
import logging
from progress.bar import Bar

CYCLES = 20

progressbar = Bar(message='Processing',
                  suffix='%(index)d/%(max)d - remain: %(remaining).2d'
                  ' - %(percent).1f%% - %(eta)ds',
                  max=CYCLES)

# create logger with 'progress bar'
logger = logging.getLogger('progress bar')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('test_out.log')
# create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handler to logger
logger.addHandler(fh)

for i in range(CYCLES):
    random_number = random.random()
    if random_number < 0.3:
        logger.info("random for index %d ok", i)
    elif random_number >= 0.3 and random_number < 0.6:
        logger.warn("random for index %d high", i)
    else:
        logger.critical("random for index %d too high", i)
    time.sleep(random_number)
    progressbar.next()
progressbar.finish()

# Example test_out.log
# 2017-05-26 14:11:24,586 - progress bar - CRITICAL - random for index 0 too high
# 2017-05-26 14:11:25,477 - progress bar - CRITICAL - random for index 1 too high
# 2017-05-26 14:11:26,437 - progress bar - CRITICAL - random for index 2 too high
# 2017-05-26 14:11:27,196 - progress bar - CRITICAL - random for index 3 too high
# 2017-05-26 14:11:28,181 - progress bar - CRITICAL - random for index 4 too high
# 2017-05-26 14:11:28,786 - progress bar - CRITICAL - random for index 5 too high
# 2017-05-26 14:11:29,562 - progress bar - WARNING - random for index 6 high
# 2017-05-26 14:11:29,941 - progress bar - WARNING - random for index 7 high
# 2017-05-26 14:11:30,266 - progress bar - WARNING - random for index 8 high
# 2017-05-26 14:11:30,763 - progress bar - CRITICAL - random for index 9 too high
# 2017-05-26 14:11:31,579 - progress bar - INFO - random for index 10 ok
# 2017-05-26 14:11:31,690 - progress bar - WARNING - random for index 11 high
# 2017-05-26 14:11:32,046 - progress bar - INFO - random for index 12 ok
# 2017-05-26 14:11:32,124 - progress bar - INFO - random for index 13 ok
# 2017-05-26 14:11:32,138 - progress bar - CRITICAL - random for index 14 too high
# 2017-05-26 14:11:32,994 - progress bar - WARNING - random for index 15 high
# 2017-05-26 14:11:33,579 - progress bar - INFO - random for index 16 ok
# 2017-05-26 14:11:33,661 - progress bar - CRITICAL - random for index 17 too high
# 2017-05-26 14:11:34,609 - progress bar - CRITICAL - random for index 18 too high
# 2017-05-26 14:11:35,395 - progress bar - INFO - random for index 19 ok
