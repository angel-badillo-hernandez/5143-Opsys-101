## 5143 Shell Project - P01

Due date: 09/25/2023

### Group Members

#### [Angel Badillo](https://github.com/It-Is-Legend27)
#### [Leslie Cook](https://github.com/Leslie-N-Cook)

### Overview:

This is a project written in Python3 that implements a basic shell that executes the UNIX commands below

### Instructions

- First, ensure all modules are installed for the shell commands by running

  `pip3 install -r requirements.txt` or `pip install -r requirements.txt`

- Next, execute the shell by running

  `python3 shell.py` or `python shell.py`

- To exit the shell, type

  `exit` or `ctrl-c`

- To run a command from the shell, type one of the commands from the list below including any flags and parameters needed

  `command -flags parameters`
  
- For more information about a command, type

  `command --help`

## Table of Commands

| Done |        Command        |                  Description                  |    Author    |             Flags             |            Parameters            |
| :--: | :--------------------: | :-------------------------------------------: | :-----------: | :---------------------------: | :-------------------------------: |
|  ✅  |    [ls](cmd_pkg/Ls.py)    |               directory listing               | Angel, Leslie | `-l` `-a` `-h` `-lah` |          `<dir name>`          |
|  ✅  |   [pwd](cmd_pkg/Pwd.py)   |            print working directory            |     Angel     |                              |                                  |
|  ✅  |    [cd](cmd_pkg/Cd.py)    |               change directory               |     Angel     |                              | `~` or `..` or `<dir name>` |
|  ✅  |   [cat](cmd_pkg/Cat.py)   |               concatenate files               |     Angel     |                              |          `<file name>`          |
|  ✅  |     [exit](shell.py)     |                  exit shell                  |     Angel     |                              |                                  |
|  ✅  | [mdkir](cmd_pkg/Mkdir.py) |             makes a new directory             |     Angel     |                              |          `<dir name>`          |
|  ✅  |   [who](cmd_pkg/Who.py)   |             show users logged in             |     Angel     |                              |                                  |
|  ✅  |  [sort](cmd_pkg/Sort.py)  |                   sort data                   |     Angel     |                              |          `<file name>`          |
|  ✅  |  [rmdir](cmd_pkg/Rmdir)  |            remove empty directory            |     Angel     |                              |          `<dir name>`          |
|  ✅  |    [rm](cmd_pkg/Rm.py)    |           remove file / directories           |     Angel     |            `-r`            | `<dir name>` or `<file name>` |
|  ✅  |    [history](shell.py)    |             show command history             | Leslie, Angel |                              |             `<num>`             |
|  ✅  |      [!x](shell.py)      |   retrieve command from history and run it   |     Angel     |                              |             `<num>`             |
|  ✅  |    [wc](cmd_pkg/Wc.py)    |   show line, word, and byte count of files   |     Angel     |     `-l` `-m` `-w`     |          `<file name>`          |
|  ✅  | [clear](cmd_pkg/Clear.py) |               clears the screen               |     Angel     |                              |                                  |
|  ✅  |    [cp](cmd_pkg/Cp.py)    |           copy file/dir to new path           |     Angel     |                              |     `<file/dir> <new path>`     |
|  ✅  |    [mv](cmd_pkg/Mv.py)    |           move file/dir to new path           |     Angel     |                              |     `<file/dir> <new path>`     |
|  ✅  | [touch](cmd_pkg/Touch.py) |             creates an empty file             |    Leslie    |                              |        `<new file name>`        |
|  ✅  | [chmod](cmd_pkg/Chmod.py) |  changes read, write, executable permissions  |    Leslie    |                              |  `<octal number> <file name>`  |
|  ✅  |  [grep](cmd_pkg/Grep.py)  | searches for a specific pattern of characters |    Leslie    | `-c` `-i` `-v ` `-l` |     `<pattern> <file path>`     |
|  ✅  |  [head](cmd_pkg/Head.py)  | writes to stdout the first 10 lines of a file |    Leslie    |       `-n, n is int`       |        `<path to file>`        |
|  ✅  |  [tail](cmd_pkg/Tail.py)  | writes to stdout the last 10 lines of a file |    Leslie    |       `-n, n is int`       |        `<path to file>`        |
|  ✅  |  [less](cmd_pkg/Less.py)  |      shows files contents on one screen      |    Leslie    |                              |        ` <path to file>`        |

## Table of support functions
|        Function        |                  Description                  |
| :--------------------: | :-------------------------------------------: |
| [getch](getch.py)   | captures the users input for the shell |
| [ParseCommand](ParseCommand.py)| parses the command line input into a list of commands  to handle pipes and redirects |
| [shell](shell.py) | main program that launches the shell |
| [init](cmd_pkg/__init__.py) | packages each commands in [cmd_pkg](cmd_pkg) to use in the shell | 
| [InvalidFlagMsg](cmd_pkg/InvalidFlagMsg.py) | creates error message when a flag not recognized |        
| [TokenizeFlags](cmd_pkg/TokenizeFlags.py) | checks for flags to direct the command behavior |  

***References***

- [Python format size application (converting B to KB, MB, GB, TB) - Stack Overflow](https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb)
- [How to to split a list at a certain value](https://stackoverflow.com/a/30538599)
