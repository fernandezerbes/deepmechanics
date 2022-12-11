from setuptools import setup

setup(
    name="deepmechanics",
    version="0.1",
    description="Deep learning methods for the solution of structural mechanics problems",
    url="https://github.com/FernandezErbes/deepmechanics",
    author="Federico Fernández Erbes",
    author_email="fernandezerbes@gmail.com",
    license="MIT",
    packages=["deepmechanics"],
    python_requires=">=3",
    install_requires=["torch>=1.4.0", "numpy>=1.18.1", "matplotlib>=3.2.2"],
    zip_safe=False,
)
