from distutils.core import setup

setup(
    name='SeMon',
    version='0.1-6-g29db280-131008230022',
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
