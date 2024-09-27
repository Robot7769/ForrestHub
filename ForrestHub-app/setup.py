from setuptools import setup, find_packages

setup(
    name='ForrestHub App',
    version='1.3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-socketio',
        'python-socketio',
        'eventlet'
    ],
    entry_points={
        'forrestHub': [
            'forrestHub = run:app.run'
        ]
    }
)
