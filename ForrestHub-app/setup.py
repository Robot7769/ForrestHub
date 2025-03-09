from setuptools import setup, find_packages

# get install_requires from requirements.txt
def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='ForrestHub App',
    version='1.4.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    entry_points={
        'forrestHub': [
            'forrestHub = run:app.run'
        ]
    }
)
