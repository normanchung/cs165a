README:

To run the provided gobang-baseline.jar file you need to type the following command in a terminal:

java -jar gobang-baseline.jar [-n <board_size>] [-l] [-d <minimax_depth>]

where board_size is an optional parameter for the board size (which should be a number between 5 and 26 (inclusive) -- default value is 11), -l is an optional flag that specified if you want the human player to play as the Light player (default behavior is that the human player gets the dark color), and minimax_depth is the desired non negative depth of minimax (0 is random -- default value is 2).

Execution examples:
java -jar gobang-baseline.jar
java -jar gobang-baseline.jar -l
java -jar gobang-baseline.jar -l -n 4
java -jar gobang-baseline.jar -l -d 3 -n 4
java -jar gobang-baseline.jar -n 8
java -jar gobang-baseline.jar -d 3 -n 16


To execute the referee program you need to type the following command:

python referee.py <board_size> <light_executable> <dark_executable>

where board_size is a number between 5 and 26, light_executable is the path to the executable of the Light player, and dark_executable is the path to the executable of the Dark player. If the code of a program is not in C/C++ you need to have an executable wrapper script that executes your java or python code and provide this script as an argument to the referee (don't forget to include this wrapper script in your submission and make sure it runs in CSIL).

As an example, we provide the script for gobang-baseline.jar, named "gobang-baseline". Make sure to actually make it executable after you download it using the chmod +x command.

The referee script also produces two files named Dark.out and Light.out that contain the consumed output of each corresponding player.

To have the gobang-baseline.jar program play Gobang with itself, you can type:

python referee.py 6 ./gobang-baseline ./gobang-baseline
