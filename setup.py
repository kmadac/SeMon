from distutils.core import setup

setup(
    name='SeMon',
    version='0.1-131006233432',
    packages=['SeMon', 'Web'],
    url='https://github.com/kmadac/SeMonWeb',
    license='',
    author='Kamil Madac',
    author_email='kamil.madac@gmail.com',
    description='Simple Server Monitoring with Dashboard',
    requires=['fabric', 'flask_bootstrap']
)
