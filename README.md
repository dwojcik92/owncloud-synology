# Fixing problems

A change in the `/lib/private/Installer.php` file may help.
Just edit: `lib/private/Installer.php`, line `274`. Change `120` to `300`.
```
$client->get($app['releases'][0]['download'], ['save_to' => $tempFile, 'timeout' => 300]);
```

a better fix is to change a line above:
```
$timeout = $this->isCLI ? 0 : 120;
```
to:
```
$timeout = $this->isCLI ? 0 : 300;
```


will fix the problem with
```
cURL error 28: Operation timed out after 120000 milliseconds with 835145 out of 2365204 bytes received (see https://curl.haxx.se/libcurl/c/libcurl-errors.html) 
```

