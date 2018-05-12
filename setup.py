from setuptools import setup

setup(
    name = 'aws_practice',
    version = '0.1',
    author = 'Nandeeswara Reddy',
    author_email = 'nanddhu4u@gmail.com',
    description = 'aws_practice is atoll to manage Iaas AWS',
    license = 'GLPv3+',
    packages = ['pratice_test'],
    url = 'https://github.com/Nandeeshkoncha/Practice_python_aws',
    install_requires = [
        'click',
        'boto3'
    ],
    entry_points = '''
        [console_scripts]
        pratice_test = pratice_test.pratice_test:cli
        ''',
)
