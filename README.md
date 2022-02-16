# Python Interactive CMD Runner
A simple beginner-friendly python library that allows the easy automation of command-line utilities in a subprocess

- run single commands (ex. ```echo this is a test```)
- run interactive commands or programs that require writing to stdin and reading from stdout

## Useage

To run a command, import the python file then create an instance of the ```script_interface(command)``` class with the command passed as a string to the constructor. Depending on what you want to do you can wait for the program to write to stdout, write to stdin, or wait for the program to finish executing.

## Methods

### ```write(stuff)```

This writes the string passed to the method to the stdin pipe of the running process

### ```read()```

This is a non-blocking read method that will return a line from the stdout pipe of the running process or "nothing found" if nothing was found

### ```read_all()```

This method reads all of the lines that the program has written to stdout. The lines are merely concatenated and still have the original whitespace and newlines.

### ```yeild_to()```

Allows the other process (or other processes, it's not deterministic) to execute.

### ```get_response(timeout=10)```

This is a blocking read method that will return the first line it reads from the subprocess or "nothing found" if nothing was returned before the timeout.

### ```is_finished()```

Return True if the subprocess has finished, otherwise false

### ```wait(timeout=100)```

Blocking method that waits until the subprocess has finished execution or the timeout has been reached.

### ```close()```

Close all of the subprocess pipes and terminate the thread.

### ```clear()```

Clear the output buffer. This can be useful for ensuring that the next output will be the expected output when interacting with the subprocess using ```write(stuff)```.
