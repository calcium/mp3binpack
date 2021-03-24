# mp3binpack
Put all your mp3s in a directory.
You run this and it will move the mp3s into directories 00, 01 etc...
which will each contain the max songs as per the number of max seconds.

For example, if you have 100 songs in a directory, and you set the max seconds per directory
to say 3600 seconds (this is set in the script, I havent gotten around to making it a command
line argument), you run the script and it will produce a series of subdirectories,
00, 01, 02 etc.. where each directory will contain songs totalling <= 3600 seconds.
That last subdirectory will contain whatever is leftover.

Currently number of seconds is set in the source code at the top.
