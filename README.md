# Fixing problems

A change in the `/lib/private/Installer.php` file may help
```
$ timeout = $ this-> isCLI? 0: 120; for example: 300
```
will fix the problem with
```
cURL error 28: Operation timed out after 120000 milliseconds with 835145 out of 2365204 bytes received (see https://curl.haxx.se/libcurl/c/libcurl-errors.html) 
```

