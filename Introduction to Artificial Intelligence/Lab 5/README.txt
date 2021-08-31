README.txt

Run this software from IDLE (available from python.org) for Python 3.x,
unless you know how to configure Tkinter to run under other environments
such as PyCharm, etc.  If you are making changes to the files, you can
always edit in PyCharm and run from IDLE, and you won't have to configure
PyCharm differently.

This is Version 9 (released Feb. 10, 2021) of the support code
for Assignment 5 in CSE 415, University of Washington, Winter 2021.

The only changes from Version 8 (Feb. 2018) have to do with file
naming, so no editing will be necessary for importing from
TOH_MDP.py.

Written by S. Tanimoto, with feedback from R. Thompson, for CSE 415
and from students in the class.

To start the GUI, type the following, in the same folder
as the code.

python3 TOH_MDP.py

As in the previous release ...

Note that the sample script suggests how to automate setup for doing
Q-Learning experiments.

The user can only show a policy when it is safe (a policy can be extracted),
assuming your extract_policy methods work.

Policy display is persistent with automatic updating whenever Q values
change.

Independent policies are stored and displayed... one for VI and one for
QL.  This also means you can view both at the same time, in different
colors.

