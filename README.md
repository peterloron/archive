# Archive
I had a need to selectively move old files from one volume to another while maintaining the directory structure. The script needed to run in the shell on our Synology NAS. I didn't find anything off the shelf which exactly fit what we needed, so I whipped this up. The files are moved based on last access time, not creation time.

The only dependency is a recent (2.7.x) version of Python.

The script is invoked like so:

archive.py -a90 -s/foo/bar -d/zoo/bar -t6

This will move all files/folders in the /foo/bar directory tree to the /zoo/bar tree which have not been accessed in the last 90 days. There will be 6 threads created to handle the copying tasks.

The archive_test.py script creates a directory structure of files and folders and then runs archive.py to validate proper operation.
