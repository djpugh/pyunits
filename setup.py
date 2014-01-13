from distutils.core import setup as setup
__doc__="""setup.py

Setup module for installing pyunitsconvert to the default third party location.

Call from command line as: python setup.py install
"""
def setupPackage(install=False):
    """setupPackage()

    Function to call distutils setup to install the package to the default location for third party modules.
    """
    setup(name='pyunitsconvert',
    version='1.0.0',
    description='Python Units Conversion for converting between different units',
    author='David Pugh',
    author_email='djpugh@gmail.com',
    package_dir={'pyunitsconvert':'.'},
    packages=['pyunitsconvert'])
if __name__=="__main__":
    setupPackage()