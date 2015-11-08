#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migrates files older than specified date from source to destination.

"""
import argparse
import os
import logging
import datetime
import time
import shutil
import random
from threading import Thread
from Queue import Queue

parser = argparse.ArgumentParser(description='Moves old files to a new location.')

parser.add_argument('-a', action="store", dest="age", default=90, type=int)
parser.add_argument('-s', action="store", dest="source_root")
parser.add_argument('-d', action="store", dest="dest_root")
parser.add_argument('-n', action="store_true", dest="no_op", default=False)
parser.add_argument('-t', action="store", dest="num_worker_threads", default=5, type=int)
parser.add_argument('--debug', action="store_true", dest="debug_mode", default=False)

shouldIKeepGoing = True
random.seed()

LOG_FILENAME = './archive.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


# Thread worker. Handles copying the file
def fileHandler(thread_id, args, q):
    global shouldIKeepGoing
    while shouldIKeepGoing:
        (source_target, dest_target) = q.get()

        if not args.no_op:
            try:
                shutil.move(source_target, dest_target)
            except Exception, err:
                logging.error("Failure while moving file -- %s" % err)
                exit()

        logging.info("[%d]Moved: %s to %s" % (thread_id, source_target, dest_target))
        if args.debug_mode:
            print("[%d]Moved: %s to %s" % (thread_id, source_target, dest_target))

        q.task_done()


def main():
    global shouldIKeepGoing
    args = parser.parse_args()
    count = 0
    AGE_INTERVAL = datetime.timedelta(days=args.age)
    NOW = datetime.datetime.now()
    file_queue = Queue()

    logging.info("***************************************************************")
    logging.info("Starting archive run at %s" % time.strftime("%c"))
    logging.info("Source: %s" % args.source_root)
    logging.info("Dest: %s" % args.dest_root)
    logging.info("Age cutoff: %d" % args.age)

    # Go through the files in the directory and see if any need to be moved
    try:
        # fire up some worker threads
        for i in range(args.num_worker_threads):
            worker = Thread(target=fileHandler, args=(i, args, file_queue,))
            worker.setDaemon(True)
            worker.start()

        for root, dirs, files in os.walk(str(args.source_root), topdown=False):
            logging.info("Checking %s..." % root)
            for thefile in files:
                count = count + 1
                source_target = os.path.join(root, thefile)

                if os.path.islink(source_target):
                    break

                stats = os.stat(source_target)
                mod_date = datetime.datetime.fromtimestamp(stats.st_mtime)
                acc_date = datetime.datetime.fromtimestamp(stats.st_mtime)

                if args.debug_mode:
                    print("Source: %s" % source_target)
                    print("ATIME: %s" % acc_date.strftime("%c"))
                    print("MTIME: %s" % mod_date.strftime("%c"))

                if (NOW - acc_date) > AGE_INTERVAL:
                    dest_target_path = os.path.join(args.dest_root, os.path.relpath(root, args.source_root))
                    dest_target = os.path.join(dest_target_path, thefile)

                    # create the directory if needed
                    if not os.path.exists(dest_target_path):
                        if not args.no_op:
                            os.makedirs(dest_target_path)
                        logging.info("Created dir: %s" % (dest_target_path))
                        if args.debug_mode:
                            print("Created dir: %s" % (dest_target_path))

                    # add to queue
                    file_queue.put((source_target, dest_target))

                # wait for threads to be done processing the queue items
                while not file_queue.empty():
                    time.sleep(0.1)

            # Go through the directories and remove them if we can
            for thedir in dirs:
                target = os.path.join(root, thedir)
                try:
                    if args.debug_mode:
                        print("Removing directory: %s" % target)
                    if not args.no_op:
                        os.rmdir(target)
                    logging.info("Removed directory: %s" % target)
                except OSError, err:
                    if args.debug_mode:
                        print("RMDIR Failed: %s" % err)
                    continue

            # finally, check the root source directory to see if it is now empty and can be removed.
            try:
                if args.debug_mode:
                    print("Removing directory: %s" % root)
                if not args.no_op:
                    os.rmdir(root)
                logging.info("Removed directory: %s" % root)
            except OSError, err:
                if args.debug_mode:
                    print("RMDIR Failed: %s" % err)

        logging.info("Processed %d files in %d seconds." % (count, (datetime.datetime.now() - NOW).seconds))
        logging.info("Done.")
    except KeyboardInterrupt:
        shouldIKeepGoing = False
        raise
    except Exception, err:
        logging.error("Failure -- %s" % err)
        exit()

# Start program
if __name__ == "__main__":
    main()
