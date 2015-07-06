from setuptools import setup

setup(
    name='petroglyph',
    version='0.4.1',
    description='A static blog generator',
    url='https://github.com/polybuildr/petroglyph',
    author='Vivek Ghaisas',
    license='MIT',
    keywords='static blog',
    packages=['petroglyph'],
    install_requires=['mistune', 'pyyaml', 'docutils'],
    include_package_data=True,
    scripts=['petroglyph/petroglyph']
)
