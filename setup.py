import glob
import io
import os
import sys

import setuptools
from setuptools import find_namespace_packages, find_packages

# Package metadata.
# name = "vortex-python"
# description = (
#     "A simple util to get a spark and mlflow session objects from an .env file"
# )

# package_root = os.path.abspath(os.path.dirname(__file__))

# version = {}
# with open(os.path.join(package_root, "version.py")) as fp:
#     exec(fp.read(), version)
# version = version["__version__"]

# readme_filename = os.path.join(package_root, "README.md")
# with io.open(readme_filename, encoding="utf-8") as readme_file:
#     readme = readme_file.read()

# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 3 - Alpha"

# with open("requirements.txt") as f:
#     required = f.read().splitlines()


# # if sys.version_info < (3, 8):
# #     find_namespace_packages()
# #     print("Error: vortex does not support this version of Python.")
# #     print("Please upgrade to Python 3.8 or higher.")
# #     sys.exit(1)


# def prepare_data_files(directory, extensions):
#     files = []
#     for ext in extensions:
#         files.extend(glob.glob(f"{directory}/*.{ext}"))
#     return files


# data_files_structure = [
#     (
#         "vortex",
#         prepare_data_files(
#             "vortex",
#             ["csv", "sql", "txt", "md", "html", "css", "json", "yaml", "faiss", "pkl"],
#         ),
#     ),
# ]


# setuptools.setup(
#     name="vortex-python",
#     packages=find_packages(exclude=["vortex_tests"]),
#     install_requires=[
#         "dagster",
#         "dagster-cloud",
#         "boto3",
#         "pandas",
#         "matplotlib",
#         "langchain",
#         "langchain_openai",
#         "openai",
#         "sqlalchemy",
#         "psycopg2-binary",
#         "pyautogen",
#         "bs4",
#         "langchainhub",
#         "langchain-community",
#         "selenium",
#         "html2text",
#         "chainlit",
#         "faiss-cpu",
#         "chromadb",
#         "tiktoken",
#         "pymupdf",
#         # "duckduckgo",
#         "wikipedia",
#         "sendgrid",
#     ],
#     extras_require={"dev": ["dagster-webserver", "pytest"]},
# )


setuptools.setup(
    name="vortex-python",
    version="0.1.2",
    description="Versatile Orchestrated Execution Engine for Data & AI Pipelines",
    # long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos D. Escobar-Valbuena",
    author_email="carlosdavidescobar@gmail.com",
    license="MIT",
    classifiers=[
        release_status,
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python" "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=["vortex_tests"]),
    install_requires=[
        "pydantic",
        "python-dotenv",
        "typing-extensions",
        "urllib3",
        "dagster",
        "pandas",
        "langchain",
        "langchain-openai",
        "openai",
        "sqlalchemy",
        "psycopg2-binary",
        "bs4",
        "dagster-webserver",
        "langchainhub",
        "selenium",
        "html2text",
        "chainlit",
        "chromadb",
        "tiktoken",
        "pymupdf",
        "duckduckgo-search",
        "wikipedia",
        "mlflow",
        "sendgrid",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
    python_requires=">=3.8",
    include_package_data=True,
    setup_requires=["setuptools", "wheel"],
    tests_require=["pytest"],
    test_suite="tests",
    zip_safe=False,
    url="https://github.com/Broomva/vortex",
    package_data={
        "vortex": [
            "*.json",
            "*.yaml",
            "*.sql",
            "*.csv",
            "*.txt",
            "*.md",
            "*.html",
            "*.css",
            "*.pkl",
            "*.faiss",
        ],
    },
    # data_files=data_files_structure,
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "vortex=main:main",
        ],
    },
)
