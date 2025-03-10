from setuptools import setup, find_packages
from pathlib import Path

__version__ = (Path(__file__).parent / "VERSION").read_text().strip()

# get install_requires from requirements.txt
def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='ForrestHub App',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    entry_points={
        'forrestHub': [
            'forrestHub = run:app.run'
        ]
    }
)
