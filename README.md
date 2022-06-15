# File sort

[![MIT license](https://img.shields.io/github/license/appuchias/file_sort?style=flat-square)](https://github.com/appuchias/file_sort/blob/master/LICENSE)
[![Author](https://img.shields.io/badge/Project%20by-Appu-9cf?style=flat-square)](https://github.com/appuchias)
![Size](https://img.shields.io/github/repo-size/appuchias/file_sort?color=orange&style=flat-square)

Repo to automatically sort any folder by file types. **Untested in half a year, I have improved my way of writing code so this can be better. It's in my to-do list**

## How it works

It will automatically move all the files and folders inside the specified root folder into the specific subfolders depending on their extension (if applicable).
It will also move all existing folder inside 'Folder' and remove any empty folder it finds.

Relations file is filled with extensions. More will be added if needed or requested.

Every change that happens, file ommited or error found will be printed to the terminal.

## Setup

1. Navigate to the folder where you want the repo to be (NOT the folder to be sorted): `cd <path>`
1. Clone the repo: `git clone https://github.com/appuchias/file_sort.git`
1. Navigate into the repo folder: `cd file_sort`
1. Run the file and add the path instead of `<path>`: `python main.py -p <path>`
1. For more info, run `python main.py -h`

## License

This project is licensed under the [MIT license](https://github.com/appuchias/file_sort/blob/master/LICENSE).

Coded with 🖤 by Appu
