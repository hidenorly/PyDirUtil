# PyDirUtil

## filename2csv.py

```
$ python3 filename2csv.py .
.,LICENSE
.,README.md
.,.gitignore
.,filename2csv.py
./.git,config
./.git,HEAD
./.git,description
./.git,index
./.git,packed-refs
./.git,COMMIT_EDITMSG
..snip..
```

## duplicateFileEnumerator.py

```
$ python3 duplicateFileEnumerator.py .
./.git/logs/HEAD,./.git/logs/refs/heads/main
./.git/refs/heads/main,./.git/refs/remotes/origin/main
```

## duplicateFileEnumerator.py

```
$ python3 duplicateFileDeleter.py .
delete ./.git/logs/HEAD due to duplication with ./.git/logs/refs/heads/main
delete ./.git/refs/heads/main due to duplication with ./.git/refs/remotes/origin/main
```

Note that this will NOT delete the files if it's without ```--actualDelete```
Just the candidate files are output.