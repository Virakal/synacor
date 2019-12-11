from pathlib import Path

from synacor import VM

if __name__ == '__main__':
    try:
        import numpy
    except ImportError:
        print('Not using numpy.')

    vm = VM()
    path = Path('spec/challenge.bin')
    vm.run(path.absolute())
