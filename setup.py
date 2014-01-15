from distutils.core import setup as setup
__doc__="""setup.py

Setup module for installing pyunits to the default third party location.

Call from command line as: python setup.py install
"""
def setupPackage(install=False):
    """setupPackage()

    Function to call distutils setup to install the package to the default location for third party modules.
    """
    setup(name='pyunits',
    version='1.0.0',
    description='Python Units for working with and converting between different units',
    author='David Pugh',
    author_email='djpugh@gmail.com',
    package_dir={'pyunits':'.'},
    packages=['pyunits'])
if __name__=="__main__":
    setupPackage()