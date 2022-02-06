# Modularize the process
# Return strings or do manipulations here,
# ask to do so from cmd or gui

# referenced:
# https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python

import os
from colorama import Fore, Style, init

infile_markers = ['Dart']
new_chunk = 'toreplacewith'
filetypes = ['.gd']
ignore_markers = ['.git']

basedir = "."

# for colorama
init()


def get_cur_comparison(startpath: str):
    end_text = ""
    for root, dirs, files in os.walk(startpath):
        # ignore dirs containing these
        for m in ignore_markers:
            if m in dirs:
                dirs.remove(m)
        # preparing for indents and printing as a tree
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * (level)
        end_text += '{}{}/'.format(indent, os.path.basename(root)) + '\n'
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            # only interested in specified filetypes
            if any(ft in f for ft in filetypes):
                contains_changes = False 
                toread = open(os.path.join(root, f), "r",
                              encoding="utf8", errors="ignore")
                for line in toread:
                    if all(im in line for im in infile_markers):
                        contains_changes = True
                        end_text += Fore.BLUE + '{}{}'.format(subindent, f) + '\n'
                        infoindent = subindent + ' ' * 2
                        end_text += Fore.RED + 'old: ' + \
                            '{}{}'.format(infoindent, line).replace(
                                '\n', '') + '\n'
                        new_line = line.replace(infile_markers[0], new_chunk)
                        end_text += Fore.GREEN + 'new: ' + \
                            '{}{}'.format(
                                infoindent, new_line).replace('\n', '') + '\n'
                        end_text += Style.RESET_ALL + '\n'
                if not contains_changes: 
                    end_text += Style.RESET_ALL + '{}{}'.format(subindent, f) + '\n'
    return end_text


def get_cur_comparison_clean(startpath: str):
    end_text = ""
    for root, dirs, files in os.walk(startpath):
        # ignore dirs containing these
        for m in ignore_markers:
            if m in dirs:
                dirs.remove(m)
        for f in files:
            # only interested in specified filetypes
            if any(ft in f for ft in filetypes):
                toread = open(os.path.join(root, f), "r",
                              encoding="utf8", errors="ignore")
                for line in toread:
                    if all(im in line for im in infile_markers):
                        end_text += '\n'
                        end_text += Fore.BLUE + f.replace('\n', '') + '\n'
                        end_text += Fore.RED + 'old: ' + \
                            line.replace('\n', '') + '\n'
                        new_line = line.replace(infile_markers[0], new_chunk)
                        end_text += Fore.GREEN + 'new: ' + new_line
                        end_text += Style.RESET_ALL
    if end_text == "":
        return "No matches found."
    else:
        return end_text

def execute_replacement(startpath: str):
    replacement_report = ""
    for root, dirs, files in os.walk(startpath):
        # ignore dirs containing these
        for m in ignore_markers:
            if m in dirs:
                dirs.remove(m)
        for f in files:
            # only interested in specified filetypes
            if any(ft in f for ft in filetypes):
                toread = open(os.path.join(root, f), "r",
                              encoding="utf8", errors="ignore")
                replacement = ""
                for line in toread:
                    if all(im in line for im in infile_markers):
                        new_line = line.replace(infile_markers[0], new_chunk)
                        replacement = replacement + new_line
                        replacement_report += Fore.BLUE + new_line
                    else:
                        replacement = replacement + line
                toread.close()
                fout = open(os.path.join(root, f), "w")
                fout.write(replacement)
                fout.close()
    return replacement_report