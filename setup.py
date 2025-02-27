from setuptools import setup, find_packages

setup(
    name="mytodo",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',  # Spezifische Version für requests
        'pyinstaller>=6.12.0'  # Für das Erstellen der exe
    ],
    entry_points={
        'console_scripts': [
            'mytodo=run:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern TODO application",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mytodo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 