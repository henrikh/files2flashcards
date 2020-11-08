import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="files2flashcards",
    version="0.0.0",
    author="Henrik Enggaard Hansen",
    author_email="henrik.enggaard@gmail.com",
    description="Keep your flashcards rooted in the context of your notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henrikh/files2flashcards",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    python_requires='>=3.6',
)
