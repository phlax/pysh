
import sys
from setuptools import Command

from .runner import PyshRunner


class PyshCommand(object):
    """A custom command to run Pylint on all Python source files."""

    description = 'Wrap system calls and prettify output, tracking failure'
    user_options = []

    def run(self, *args, **kwargs):
        """Run command."""
        # ...mangle... args
        #
        command = args[0]
        PyshRunner().run(command)


def main():
    PyshCommand().run(*sys.argv[1:])


if __name__ == "__main__":
    main()
