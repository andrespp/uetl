from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='uetl',
    version='0.1.2',
    description='Minimalist python ETL library.',
    py_modules=["uetl"],
    package_dir={'':'src'},
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ["pandas >= 0.2",
                        "pyodbc >= 4.0",
                        "SQLAlchemy >= 1.3",
                        "psycopg2 >= 2.8",
                       ],
    extras_require = {
        "dev": ["check-manifest",
                "pytest>=3.7",
                "twine",
                "tox",
               ],
    },
    #sdist requirements
    url="https://github.com/andrespp/uetl",
    author="Andre Pereira",
    author_email="andrespp@gmail.com",
)
