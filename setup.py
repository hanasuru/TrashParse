from distutils.core import setup
setup(
  name = 'trashparse',
  packages = ['trashparse'],
  version = '0.1.1',
  license='MIT',
  description = 'simple tool for analyzing Windows Recycle.Bin',
  author = 'hanasuru',
  author_email = 'faqih.insani@ymail.com',
  url = 'https://github.com/hanasuru/TrashParse',
  download_url = 'https://github.com/hanasuru/TrashParse/archive/0.1.1.tar.gz',
  keywords = ['forensic', 'recycle-bin', 'windows'],
  install_requires=['prettytable'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
  ],
  scripts=['bin/trashparse'],
)
