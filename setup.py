import glob
import os
import shutil
from pathlib import Path

from setuptools import setup, find_packages, Command


HERE = Path(os.path.dirname(__file__)).absolute()
# get __version__ from periodicity_detection/_version.py
with open(HERE / "periodicity_detection" / "_version.py") as fh:
    exec(fh.read())
VERSION: str = __version__  # noqa
README = (HERE / "README.md").read_text(encoding="UTF-8")
PYTHON_NAME = "periodicity_detection"


class CleanCommand(Command):
    description = "Remove build artifacts from the source tree"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        files = [".coverage*", "coverage.xml"]
        dirs = [
            "build",
            "dist",
            "*.egg-info",
            "**/__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            "**/.ipynb_checkpoints",
        ]
        for d in dirs:
            for filename in glob.glob(d):
                shutil.rmtree(filename, ignore_errors=True)

        for f in files:
            for filename in glob.glob(f):
                try:
                    os.remove(filename)
                except OSError:
                    pass


if __name__ == "__main__":
    setup(
        name=PYTHON_NAME,
        version=VERSION,
        long_description=README,
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=("tests", "tests.*")),
        package_data={"periodicity_detection": ["py.typed"]},
        test_suite="tests",
        cmdclass={
            "clean": CleanCommand,
        },
        zip_safe=False,
        entry_points={
            "console_scripts": ["periodicity=periodicity_detection.__main__:cli"]
        },
    )
