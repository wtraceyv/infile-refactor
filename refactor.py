import os 
import sys
from colorama import Fore, Style, init

infile_markers = ['totarget']
new_chunk = 'toreplacewith'
filetypes = ['.gd']
ignore_markers = ['.git']

basedir = "."

# for colorama
init()

# referenced:
# https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
def print_cur_comparison(startpath: str):
	for root, dirs, files in os.walk(startpath):
		# ignore dirs containing these
		for m in ignore_markers:
			if m in dirs:
				dirs.remove(m)
		# preparing for indents and printing as a tree
		level = root.replace(startpath, '').count(os.sep)
		indent = ' ' * 2 * (level)
		print('{}{}/'.format(indent, os.path.basename(root)))
		subindent = ' ' * 2 * (level + 1)
		for f in files:
			# only interested in specified filetypes 
			if any(ft in f for ft in filetypes):
				print('{}{}'.format(subindent, f))
				toread = open(os.path.join(root, f), "r", encoding="utf8", errors="ignore")
				for line in toread:
					if all(im in line for im in infile_markers):
						infoindent = subindent + ' ' * 2 
						print(Fore.RED + 'old: ' + '{}{}'.format(infoindent, line).replace('\n', ''))
						new_line = line.replace(infile_markers[0], new_chunk)
						print(Fore.GREEN + 'new: ' + '{}{}'.format(infoindent, new_line).replace('\n', ''))
						print(Style.RESET_ALL)

def print_cur_comparison_clean(startpath: str):
	for root, dirs, files in os.walk(startpath):
		# ignore dirs containing these
		for m in ignore_markers:
			if m in dirs:
				dirs.remove(m)
		for f in files:
			# only interested in specified filetypes 
			if any(ft in f for ft in filetypes):
				toread = open(os.path.join(root, f), "r", encoding="utf8", errors="ignore")
				for line in toread:
					if all(im in line for im in infile_markers):
						print(Fore.BLUE + f.replace('\n', ''))
						print(Fore.RED + 'old: ' + line.replace('\n', ''))
						new_line = line.replace(infile_markers[0], new_chunk)
						print(Fore.GREEN + 'new: ' + new_line.replace('\n', ''))
						print(Style.RESET_ALL)

def execute_replacement(startpath: str):
	for root, dirs, files in os.walk(startpath):
		# ignore dirs containing these
		for m in ignore_markers:
			if m in dirs:
				dirs.remove(m)
		for f in files:
			# only interested in specified filetypes 
			if any(ft in f for ft in filetypes):
				toread = open(os.path.join(root, f), "r", encoding="utf8", errors="ignore")
				replacement = ""
				for line in toread:
					if all(im in line for im in infile_markers):
						new_line = line.replace(infile_markers[0], new_chunk)
						replacement = replacement + new_line
						print(Fore.BLUE + new_line.replace('\n', ''))
					else:
						replacement = replacement + line 
				toread.close()
				fout = open(os.path.join(root, f), "w")
				fout.write(replacement)
				fout.close()


def print_main_options():
	print("-----------")
	print(Fore.BLUE + "SEARCH: " + ' '.join(infile_markers) + "\nREPLACE: " + new_chunk + "\nfile types: " + ' '.join(filetypes) + "\nignored dirs: " + ' '.join(ignore_markers) + Style.RESET_ALL)
	print("(1): set blob to search for\n(2): set blob to replace target with\n(3): more search settings")
	print("(4): view current target setup\n(5): execute current replacements\n(e): exit")

def print_refine_options():
	print("***********")
	print("Current settings: ")
	print(Fore.BLUE + "SEARCH: " + ' '.join(infile_markers) + ", file types: " + ' '.join(filetypes) + ", ignored dirs: " + ' '.join(ignore_markers) + Style.RESET_ALL)
	print("(1): add blobs to search for\n(2): reset file types\n(3): add file types")
	print("(4): reset blobs to ignore\n(5): add blobs to ignore\n(e): back")

def print_show_options():
	print("***********")
	print("(1): print changes per file\n(2): print changes with directory context\n(e): back")

# user supplying different root folder
if len(sys.argv) > 1:
	print(Fore.BLUE + "Working at supplied directory " + sys.argv[1] + Style.RESET_ALL)
	basedir = sys.argv[1]
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
		infile_markers = []
		infile_markers.append(newtarget)
		print(Fore.BLUE + "New target set: " + infile_markers[0] + Style.RESET_ALL) 
	elif userin == "2":
		newreplace = input("supply new replacement: ")
		new_chunk = newreplace
		print(Fore.BLUE + "New replacement set: " + new_chunk + Style.RESET_ALL)
	elif userin == "3":
		# sub menu
		while True:
			print_refine_options()
			refineop = input(Fore.GREEN + "input option >>> " + Style.RESET_ALL)
			if refineop == "e":
				break
			elif refineop == "1":
				blobtoadd = input("supply new blob to refine search: ")
				infile_markers.append(blobtoadd)
				print(Fore.BLUE + "Added blob, new blobs used to search: " + ' '.join(infile_markers) + Style.RESET_ALL)
			elif refineop == "2":
				filetypes = [""]
				print(Fore.BLUE + "Reset file types" + Style.RESET_ALL)
			elif refineop == "3":
				ftadd = input("supply file type to add: ")
				filetypes.append(ftadd)
				print(Fore.BLUE + "Added filetype, filetypes now used in search: " + ' '.join(filetypes) + Style.RESET_ALL)
			elif refineop == "4":
				ignore_markers = []
				print(Fore.BLUE + "Reset dir ignore markers" + Style.RESET_ALL)
			elif refineop == "5":
				toignore = input("supply new dir marker to ignore: ")
				ignore_markers.append(toignore)
				print(Fore.BLUE + "Added ignore marker, ignoring following dirs in search: " + ' '.join(ignore_markers) + Style.RESET_ALL)
		# end sub menu
	elif userin == "4":
		# sub menu
		while True:
			print_show_options()
			showop = input(Fore.GREEN + "input option >>> " + Style.RESET_ALL)
			if showop == "e":
				break
			elif showop == "1":
				print_cur_comparison_clean(basedir)
			elif showop == "2":
				print_cur_comparison(basedir)
		# end sub menu	
	elif userin == "5":
		print(Fore.RED + "Finding: " + infile_markers[0])
		print("Replacing with: " + new_chunk + Style.RESET_ALL)
		confirm = input("Are you sure? (y/n): ")
		if confirm == "n":
			continue
		print(Fore.BLUE + "Executing replacements.." + Style.RESET_ALL)
		execute_replacement(basedir)
		print(Fore.BLUE + "..Done." + Style.RESET_ALL)

