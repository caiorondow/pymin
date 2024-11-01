import setuptools
import os

# Ler o conteúdo do README.md para a descrição longa
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Construir o caminho para o arquivo requirements.txt
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = os.path.join(lib_folder, 'requirements.txt')

# Ler as dependências do requirements.txt, se existir
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

# Configurar a instalação do pacote
setuptools.setup(
    name="minpy",
    version="0.1",
    author="Caio Von Rondow",
    author_email="caiorondow@gmail.com",
    description="A Python library for simulating routing in Multistage Interconnection Networks (MINs).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caiorondow/pymin.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
)