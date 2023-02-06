from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="destables",
    install_requires=[
        'PySimpleGUI>=4.56.0',
        'tabulate>=0.8.9',
        'clipboard>=0.0.4',
        'antlr4-python3-runtime==4.9.3'
    ],
    extras_require={
    },
)
