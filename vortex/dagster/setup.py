from setuptools import find_packages, setup

setup(
    name="vortex",
    packages=find_packages(exclude=["vortex_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "boto3",
        "pandas",
        "matplotlib",
        "langchain",
        "langchain_openai",
        "openai",
        "sqlalchemy",
        "psycopg2-binary",
        "pyautogen",
        "bs4",
        "langchainhub",
        "langchain-community",
        "selenium",
        "html2text",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
