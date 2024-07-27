from setuptools import setup, find_packages

setup(
    name='Forester App',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-socketio',
        'python-socketio',
        'eventlet'
    ],
    entry_points={
        'forester': [
            'forester = run:app.run'
        ]
    }
)
