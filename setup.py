import setuptools
setuptools.setup(
  name="telegram-sdk",
  version="1.0.0",
  author="Layrz",
  author_email="software@layrz.com",
  url='https://gitlab.com/layrz-software/libraries/telegram-sdk',
  license='MIT',
  description="Telegram SDK for public or private Telegram API",
  keywords='telegram api bot sdk layrz goldenm',
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires=[
    'requests'
  ],
  python_requires='>=3.8'
)
