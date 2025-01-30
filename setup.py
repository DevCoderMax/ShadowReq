from setuptools import setup, find_packages

# Lê a versão de um arquivo de texto para evitar importação circular
with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read().strip()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shadowreq",
    version=version,
    author="DevCoderMax",
    author_email="",  # Adicione seu email se desejar
    description="Uma biblioteca Python para fazer requisições HTTP através de servidores intermediários",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DevCoderMax/ShadowReq",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "selenium>=4.0.0",
        "webdriver-manager>=3.8.0",
    ],
    package_data={
        'shadowreq': ['servers.json'],
    },
    entry_points={
        'console_scripts': [
            'shadowreq=shadowreq.cli:main',
        ],
    },
)
