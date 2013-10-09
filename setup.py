from distutils.core import setup

setup(
    name='SeMon',
    version='0.1-11-gd9c9194-131009234501',
    packages=['SeMon', 'Web'],
    package_data={'Web': ['static/*', 'templates/*']},
    scripts=['bin/semond.py'],
    url='https://github.com/kmadac/SeMonWeb',
    license='',
    author='Kamil Madac',
    author_email='kamil.madac@gmail.com',
    description='Simple Server Monitoring with Dashboard',
    requires=['fabric', 'flask_bootstrap']
)
