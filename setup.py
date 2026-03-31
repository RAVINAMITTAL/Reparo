from setuptools import setup, find_packages

setup(
    name="reparo",
    version="0.1.0",
    description="Reparo — AI-assisted self-healing compiler for the Replon language",
    packages=find_packages(),
    py_modules=["reparo_cli"],
    python_requires=">=3.10",
    entry_points={
        # This is what creates the `reparo` shell command after `pip install -e .`
        "console_scripts": [
            "reparo = reparo_cli:main",
        ],
    },
)
