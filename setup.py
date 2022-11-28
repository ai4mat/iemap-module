import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='iemap',                           # should match the package folder
    packages=['iemap'],                     # should match the package folder
    version='0.2.2',                                # important for updates
    license='GPL',                                  # should match your chosen license
    description='Tools to use IEMAP Rest API',      # should match the package folder
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Marco Puccini',
    author_email='marco.puccini@enea.it',
    url='https://github.com/ai4mat/iemap-module', 
    project_urls = {                                # Optional
        "Homepage": "https://github.com/ai4mat/iemap-module",
        "Documentation": "https://github.com/ai4mat/iemap-module",
        "Bug Tracker": "https://github.com/ai4mat/iemap-module/issues"
    },
    install_requires=['requests==2.28.1', 'requests_toolbelt==0.9.1', 'bson==0.5.10'],                  # list all packages that your package uses
    keywords=["pypi", "iemap", "api"], #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        "Operating System :: OS Independent",
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.10',
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Utilities"
    ],
    
    download_url="https://github.com/ai4mat/iemap-module/archive/refs/tags/v0.2.2.tar.gz",
)