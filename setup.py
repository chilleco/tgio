from setuptools import setup, find_packages


with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name='tgio',
    version='0.1',
    description='The simplest library for Telegram bots',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kosyachniy/tgio',
    author='Alexey Poloz',
    author_email='polozhev@mail.ru',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='simple, Telegram, bot',
    packages=find_packages(exclude=('tests',)),
    python_requires='>=3.7, <4',
    install_requires=[
        'aiogram',
    ],
    project_urls={
        'Source': 'https://github.com/kosyachniy/tgio',
    },
    license='MIT',
    include_package_data=False,
)
