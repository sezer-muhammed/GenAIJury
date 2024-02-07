from setuptools import setup, find_packages
import os
setup(
    name='genaijury',
    version='0.0.1',
    author='Muhammed Sezer',
    author_email='muhammedsezer12@gmail.com',
    description='A Python package for evaluating data with AI-driven juries.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='',  # URL to the repository if available
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here
        # e.g., 'requests>=2.25.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8.1',
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            # Add other test dependencies here
        ],
    },
)
