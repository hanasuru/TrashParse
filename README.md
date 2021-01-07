# TrashParse

TrashParse is a simple tool for analyzing Windows Recycle.Bin files based on $I & $R entry. Also a tool that originally inspired from [$I parser](https://df-stream.com/recycle-bin-i-parser/).

## Installation

```
$ pip install trashparse
```


## Usage

For instances, you can check helper section by passing `-h` or `--help`.

```bash
$ trashparse -h                                                       

usage: trashparse [-h] [--sort attribute] [--write directory] [--quiet]
                  directory

Simple Recycle.Bin Windows Parser

positional arguments:
  directory             target directory

optional arguments:
  -h, --help            show this help message and exit
  --sort attribute, -s attribute
                        Sort by attribute (name, time, size)
  --write directory, -w directory
                        Write $R content into a directory; default="files/"
  --quiet, -q           quiet (Don't show list file)                                       
```

### Display general info

TrashParse allow you to generate general information by passing directory name that contains any file with `$I prefix file`

```bash
$ trashparse \$RECYCLE.BIN/S-1-5-21-4144826732-2003267707-115468498-1001

+--------------+----------------------------+------------+------+---------------------+
|    Index     |        Deleted Time        |  Version   | Size |    Original Path    |
+--------------+----------------------------+------------+------+---------------------+
| $IEW83YF.txt | 2020-11-30 22:12:27.451000 | Windows 10 |  30  | D:\samples\test.txt |
+--------------+----------------------------+------------+------+---------------------+


```

### Extract deleted file

TrashParse allow you to extract content based on parsed `fileinfo` from `$I and $R file`

```bash
$ trashparse \$RECYCLE.BIN/S-1-5-21-4144826732-2003267707-115468498-1001 -q -w files

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