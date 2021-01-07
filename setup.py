from distutils.core import setup
setup(
  name = 'trashparse',
  packages = ['trashparse'],
  version = '0.1',
  license='MIT',
  description = 'simple tool for analyzing Windows Recycle.Bin',
  author = 'hanasuru',
  author_email = 'faqih.insani@ymail.com',
  url = 'https://github.com/hanasuru/TrashParse',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hanasuru/TrashParse/archive/0.1.0.tar.gz',    # I explain this later on
  keywords = ['forensic', 'recycle-bin', 'windows'],   # Keywords that define your package best
  install_requires=['prettytable'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2.7',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
  scripts=['bin/trashparse'],
)
