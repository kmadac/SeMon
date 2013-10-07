from distutils.core import setup

setup(
    name='SeMon',
    version='0.1-1-g73c7f7a-131007221019',
    packages=['SeMon', 'Web'],
    package_data={'Web': ['static/*', 'templates/*']},
    url='https://github.com/kmadac/SeMonWeb',
    license='',
    author='Kamil Madac',
    author_email='kamil.madac@gmail.com',
    description='Simple Server Monitoring with Dashboard',
    requires=['fabric', 'flask_bootstrap']
)
