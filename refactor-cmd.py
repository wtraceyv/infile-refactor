from colorama import Fore, Style, init
import refactor
import sys

def print_main_options():
    print("-----------")
    print(Fore.BLUE + "SEARCH: " + ' '.join(refactor.infile_markers) + "\nREPLACE: " + refactor.new_chunk + "\nfile types: " +
          ' '.join(refactor.filetypes) + "\nignored dirs: " + ' '.join(refactor.ignore_markers) + Style.RESET_ALL)
    print("(1): set blob to search for\n(2): set blob to replace target with\n(3): more search settings")
    print("(4): view current target setup\n(5): execute current replacements\n(e): exit")

def print_refine_options():
    print("***********")
    print("Current settings: ")
    print(Fore.BLUE + "SEARCH: " + ' '.join(refactor.infile_markers) + ", file types: " +
          ' '.join(refactor.filetypes) + ", ignored dirs: " + ' '.join(refactor.ignore_markers) + Style.RESET_ALL)
    print("(1): add blobs to search for\n(2): reset file types\n(3): add file types")
    print("(4): reset blobs to ignore\n(5): add blobs to ignore\n(e): back")


def print_show_options():
    print("***********")
    print("(1): print changes per file\n(2): print changes with directory context\n(e): back")


# user supplying different root folder
if len(sys.argv) > 1:
    print(Fore.BLUE + "Working at supplied directory " +
          sys.argv[1] + Style.RESET_ALL)
    refactor.basedir = sys.argv[1]
else:
    print(Fore.BLUE + "Working at current directory of refactor.py" + Style.RESET_ALL)

# take some input to do these things
while True:
    print_main_options()
    userin = input(Fore.GREEN + "input option >>> " + Style.RESET_ALL)
    if userin == "e":
        break
    elif userin == "1":
        newtarget = input("supply new target: ")
        refactor.infile_markers = []
        refactor.infile_markers.append(newtarget)
        print(Fore.BLUE + "New target set: " +
              refactor.infile_markers[0] + Style.RESET_ALL)
    elif userin == "2":
        newreplace = input("supply new replacement: ")
        refactor.new_chunk = newreplace
        print(Fore.BLUE + "New replacement set: " + refactor.new_chunk + Style.RESET_ALL)
    elif userin == "3":
        # sub menu
        while True:
            print_refine_options()
            refineop = input(
                Fore.GREEN + "input option >>> " + Style.RESET_ALL)
            if refineop == "e":
                break
            elif refineop == "1":
                blobtoadd = input("supply new blob to refine search: ")
                refactor.infile_markers.append(blobtoadd)
                print(Fore.BLUE + "Added blob, new blobs used to search: " +
                      ' '.join(refactor.infile_markers) + Style.RESET_ALL)
            elif refineop == "2":
                refactor.filetypes = [""]
                print(Fore.BLUE + "Reset file types" + Style.RESET_ALL)
            elif refineop == "3":
                ftadd = input("supply file type to add: ")
                refactor.filetypes.append(ftadd)
                print(Fore.BLUE + "Added filetype, filetypes now used in search: " +
                      ' '.join(refactor.filetypes) + Style.RESET_ALL)
            elif refineop == "4":
                refactor.ignore_markers = []
                print(Fore.BLUE + "Reset dir ignore markers" + Style.RESET_ALL)
            elif refineop == "5":
                toignore = input("supply new dir marker to ignore: ")
                refactor.ignore_markers.append(toignore)
                print(Fore.BLUE + "Added ignore marker, ignoring following dirs in search: " +
                      ' '.join(refactor.ignore_markers) + Style.RESET_ALL)
        # end sub menu
    elif userin == "4":
        # sub menu
        while True:
            print_show_options()
            showop = input(Fore.GREEN + "input option >>> " + Style.RESET_ALL)
            if showop == "e":
                break
            elif showop == "1":
                print(refactor.get_cur_comparison_clean(refactor.basedir))
            elif showop == "2":
                print(refactor.get_cur_comparison(refactor.basedir))
        # end sub menu
    elif userin == "5":
        print(Fore.RED + "Finding: " + refactor.infile_markers[0])
        print("Replacing with: " + refactor.new_chunk + Style.RESET_ALL)
        confirm = input("Are you sure? (y/n): ")
        if confirm == "n":
            continue
        print(Fore.BLUE + "Executing replacements.." + Style.RESET_ALL)
        print(refactor.execute_replacement(refactor.basedir))
        print(Fore.BLUE + "..Done." + Style.RESET_ALL)
