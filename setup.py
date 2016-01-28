from setuptools import setup

setup(
    name='petroglyph',
    version='0.5.0',
    description='A static blog generator',
    url='https://github.com/polybuildr/petroglyph',
    author='Vivek Ghaisas',
    license='MIT',
    keywords='static blog',
    packages=['petroglyph'],
    install_requires=['mistune', 'pyyaml', 'docutils', 'htmlmin', 'jinja2'],
    include_package_data=True,
    scripts=['petroglyph/petroglyph']
)
