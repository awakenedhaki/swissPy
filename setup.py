import setuptools

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setuptools.setup(
    name="awakenedhaki",
    version="0.1.0",
    author="Rodrigo Vallejos",
    description="Project Euler facilitator CLI",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=['swisspy', 'swissPy', 'euler', 'project-euler', 'projecteuler'],
    license="MIT",
    classifiers=[
        "Topic :: Utilities",
    ],
    url="https://github.com/awakenedhaki/swissPy",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    entry_points={'console_scripts': ['euler = swissPy.__main__:main']}
)
