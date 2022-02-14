#!/usr/bin/env python3
import sys
import time


def flush_then_wait():
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.5)


sys.stdout.write("Script stdout 1\n")
sys.stdout.write("Script stdout 2\n")
sys.stdout.write("Script stdout 3\n")
flush_then_wait()

sys.stdout.write("name=Martin\n")
sys.stderr.write("Total time: 00:05:00\n")
sys.stdout.write("Script stdout 4\n")
sys.stdout.write("Script stdout 5\n")
sys.stderr.write("Total complete: 0%\n")
flush_then_wait()

sys.stderr.write("Elapsed time: 00:00:10\n")
sys.stderr.write("Elapsed time: 00:00:50\n")
sys.stderr.write("Total complete: 5%\n")
sys.stdout.write("country=Nederland\n")
flush_then_wait()

sys.stderr.write("Elapsed time: 00:01:10\n")
sys.stderr.write("Total complete: 10%\n")
sys.stdout.write("Script stdout 6\n")
sys.stdout.write("Script stdout 7\n")
sys.stdout.write("website=www.pythonguis.com\n")
flush_then_wait()

sys.stderr.write("Elapsed time: 00:01:20\n")
sys.stderr.write("Elapsed time: 00:02:50\n")
sys.stderr.write("Total complete: 20%\n")
sys.stdout.write("Script stdout 8\n")
sys.stdout.write("Script stdout 9\n")
flush_then_wait()

sys.stderr.write("Elapsed time: 00:02:90\n")
sys.stderr.write("Total complete: 25%\n")
sys.stderr.write("Elapsed time: 00:03:10\n")
sys.stderr.write("Total complete: 30%\n")
sys.stdout.write("Script stdout 10\n")
sys.stdout.write("Script stdout 11\n")
flush_then_wait()

sys.stderr.write("Elapsed time: 00:03:70\n")
sys.stderr.write("Total complete: 35%\n")
sys.stderr.write("Elapsed time: 00:03:90\n")
sys.stderr.write("Total complete: 45%\n")
sys.stdout.write("Script stdout 12\n")
sys.stdout.write("Script stdout 13\n")
flush_then_wait()

sys.stderr.write("Elapsed time: 00:04:10\n")
sys.stderr.write("Total complete: 65%\n")
sys.stderr.write("Elapsed time: 00:04:50\n")
sys.stderr.write("Total complete: 75%\n")
sys.stdout.write("Script stdout 14\n")
sys.stdout.write("Script stdout 15\n")
flush_then_wait()

sys.stderr.write("Elapsed time: 00:04:70\n")
sys.stderr.write("Total complete: 80%\n")
sys.stderr.write("Elapsed time: 00:04:90\n")
sys.stderr.write("Total complete: 90%\n")
sys.stdout.write("Script stdout 16\n")
sys.stdout.write("Script stdout 17\n")
flush_then_wait()

sys.stderr.write("Elapsed time: 00:05:00\n")
sys.stderr.write("Total complete: 100%\n")
sys.stdout.write("Script stdout 18\n")
sys.stdout.write("Script stdout 19\n")
flush_then_wait()
