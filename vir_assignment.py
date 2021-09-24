"""script to extract the text that matches regular expression 
within a text file

maintainer: Amin Momin (momin.amin@gmail.com)

usage: 
    - for single file: python vir_assignment.py -c abc.txt a.b+
    - for files within directory: python vir_assignment.py -r data\ johnson
      
"""
from pathlib import Path
import sys
import getopt
import re
from typing import List, Tuple


def parse_args(argvs: List[str]) -> Tuple:
    """function parses command line arguments and separate
    options and arguments. 

    Args:
        argvs (List[str]): list of all the argument on the command line

    Returns:
        Tuple: return a tuple of single file (bool), recursive search (bool),
            path (Path) and regex pattern (str)
    """

    single_file: bool = False
    recursive_search: bool = False
    input_path: Path = None
    pattern: str = None

    try:
        opts, args = getopt.getopt(argvs, "cr")

    except:
        print("Error occured")

    # parse options
    if len(opts) > 0:
        for opt, arg in opts:
            if opt in ['-c']:
                single_file = True
            elif opt in ['-r']:
                recursive_search = True
        print(
            f"single file: {single_file}, recursive_search: {recursive_search}")

    else:
        print(f"Insufficient options. Requires either -c or -r")
        sys.exit()

    # parse arguments
    try:
        input_path = Path(args[0])
        pattern = args[1]

    except:
        print(f"Insufficient arguments. Expected <path> and <regex>")
        sys.exit()

    else:
        print(f"input path: {input_path}, regex pattern: {pattern}")

    return(single_file, recursive_search, input_path, pattern)


# with open(input_file, mode='r') as INPUT, open(output_file, mode='w') as OUTPUT:
#    pass

class SearchPattern:
    """the class perform search of individual file or all files within
    a directory. It returns a list of files if the regex pattern is found
    within its content or the file name. 

    Output file: The output is written in the working directory with the 
    <redex> pattern in the file name.

    Limitations:
        - Input files: need to be text files for the reader to iterate

    """

    def __init__(self, args: List) -> None:
        """the method initializes the class using inputs from the 
        command line argument

        - Parses the command line arguments and initializes the 
            object attributes
        - Assign values for file path, regex and boolion argument 
            based on options
        - If single file then it intiate the search of the file
        - If recursive, then it searches for all the files in the 
            directory and then the regex within all files

        Args:
            args (List): [description]
        """
        self._args = args
        self._single_file, self._recursive_search, self._path, self._regex = parse_args(
            self._args)

        # output file name
        self.output_file = f"output_{self._regex}_search.txt"

        # list of files with pattern
        self._file_search: List = []

        if self._single_file:
            self._search_file(self._path)
        elif self._recursive_search:
            self._search_recursively(self._path)

    def write_file(self, output_file: Path) -> None:
        """method to write list of files with regex pattern

        Args:
            output_file (Path): output file name for regex search
        """
        if len(self._file_search) > 0:
            with open(output_file, "w") as write:
                for file, val in self._file_search:

                    write.writelines(f"{str(file)}, {val}\n")
        else:
            print(f"Sorry, couldn't find a file with the pattern")

    def _search_file(self, file_path: Path) -> None:
        """method to look for regex in individual file

        Args:
            file_path (Path): path of indiavidual file

        """
        # check pattern in file name
        if re.search(self._regex, file_path.name):
            self._file_search.append((file_path, True))
            val = True
            return

        # check pattern in file content
        with open(file_path, mode='r') as input:
            for line in input:
                if re.search(self._regex, line.strip()):
                    self._file_search.append((file_path, True))
                    return

    def _search_recursively(self, file_path: Path) -> None:
        """method to search regex recursively in a directory

        Args:
            file_path (Path): file path to directory of input files
        """
        self._all_files = self._list_files(self._path)
        if len(self._all_files) > 0:
            print(
                f"Number of files in dir and sub-dir: {len(self._all_files)}")
            # print(self._all_files)
            for file in self._all_files:
                self._search_file(file)

        else:
            print(f"No files detected in the directories")

    def _list_files(self, file_path: Path) -> List[Path]:
        """method searhes all files in a directory and returns a list

        Args:
            file_path (Path): file path for folder

        Returns:
            List[Path]: list of all files in file path
        """
        files = [file for file in file_path.iterdir() if file.is_file()]
        return files


def main():
    # parse input, initialize class and search file
    s = SearchPattern(sys.argv[1:])

    # write the list of file with pattern match
    s.write_file(s.output_file)


if __name__ == '__main__':
    main()
