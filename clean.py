import argparse
import os
import tree

def main():
    MUSIC_FORMATS = ['mp3', 'flac', 'waw', 'm4a']
    
    desc = "Script that scans folders and remove folders that do not contain music.\nSupported music formats:\n"
    
    for sformat in MUSIC_FORMATS:
        desc += "  " + sformat + "\n"
    
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('path', help='Path to music library')

    parser.add_argument('-t', '--tree', help='Prints file tree that will be deleted', action="store_true")

    args = parser.parse_args()

    empty_dirs = find_folders_not_containing(args.path, MUSIC_FORMATS)
    for folder in empty_dirs:
        if args.tree:
            tree.tree(folder, '  ', True)
        else:
            print(folder)

def find_folders_not_containing(folder, formats):
    os.chdir(folder)
    result = []
    for root, dirs, files in os.walk('.'):
        while len(dirs) > 0:
            current = dirs.pop()
            empty = is_empty_file_tree(current, formats)
            if empty:
                result.append(current)
    return result

def is_empty_file_tree(directory, formats):
    result = []
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            result.append(is_empty_file_tree(os.path.join(root, directory), formats))

        return is_dirs_empty(result) and not search_files(files, formats)

def is_dirs_empty(result_list):
    for directory in result_list:
        if directory == False:
            return False
    
    return True

def search_files(files, formats):
    for sfile in files:
        for sformat in formats:
            if sfile.endswith(sformat):
                return True;

    return False;

if __name__ == '__main__':
    main()
