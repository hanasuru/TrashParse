# TrashParse

TrashParse is a simple tool for analyzing Windows Recycle.Bin files based on $I & $R entry. Also a tool that originally inspired from [$I parser](https://df-stream.com/recycle-bin-i-parser/).

## Installation

```
$ git clone https://github.com/hanasuru/TrashParse
$ cd TrashParse/src

$ sudo ln -s `pwd`/trashparse.py /usr/local/bin/trashparse
$ sudo chmod +x /usr/local/bin/trashparse

```


## Usage

For instances, you can check helper section by passing `-h` or `--help`.

```bash
$ trashparse -h                                                       

usage: trashparse.py [-h] [--sort attribute] [--extract] [--quiet] directory

Simple Recycle.Bin Windows Parser

positional arguments:
  directory             target directory

optional arguments:
  -h, --help            show this help message and exit
  --sort attribute, -s attribute
                        Sort by attribute (name, time, size)
  --extract, -e         Extract & dump bin into files
  --quiet, -q           quiet (Don't show list file)
                                                      
```

### Display general info

TrashParse allow you to generate general information by passing directory name that contains any file with `$I and $R file`

```bash
# trashparse directory of file with $I & $R prefix
$ trashparse \$RECYCLE.BIN/S-1-5-21-4144826732-2003267707-115468498-1001

Id          Size    Original Path                           Version        Deleted Time (UTC)
EW83YF.txt  30      D:\samples\test.txt                     Windows 10     2020-11-30 22:12:27

```

### Extract deleted file

TrashParse allow you to extract content based on parsed `fileinfo` from `$I and $R file`

```bash
$ trashparse \$RECYCLE.BIN/S-1-5-21-4144826732-2003267707-115468498-1001 -e -q 

$ ls files/
test.txt

$ cat files/test.txt  
This file will be deleted soon
```

## Authors

* **hanasuru** - *Initial work* 

See also the list of [contributors](https://github.com/hanasuru/TrashParse/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details