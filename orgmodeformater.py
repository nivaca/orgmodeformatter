import os
import binascii
from shutil import copyfile

orgtags: str = ':latin:'
directory: str = ''  # local directory
extensions: list[str] = ['.org']


def generate_id() -> str:
    def genhex(n):
        return str(binascii.b2a_hex(os.urandom(n)).decode())
    return f"{genhex(4)}-{genhex(2)}-{genhex(2)}-{genhex(2)}-{genhex(6)}".lower()


def get_files() -> list[str]:
    files: list[str] = []
    allfilenames = os.listdir(directory + '.')
    for fi in allfilenames:
        ext = os.path.splitext(fi)[1]
        # check if file of proper extension
        if ext.lower() in extensions:
            files.append(fi)
    # returns a lists of file objects
    return files


def formathead() -> str:
    return f":PROPERTIES:\n" \
           f":ID:       {generate_id()}\n" \
           f":END:\n" \
           f"#+filetags: {orgtags}\n" \
           f"#+title: \n\n"


def insertid(fn):
    copyfile(fn, f'{fn}.bak')  # make a backup file
    with open(fn, mode="w") as destfile:
        destfile.write(formathead())
        with open(f'{fn}.bak') as origfile:
            for line in origfile:
                if '@' in line:
                    continue
                destfile.write(f"{line}")


def main():
    files = get_files()
    for fn in files:
        print(f"Processing {fn}...")
        insertid(fn)


if __name__ == "__main__":
    main()
