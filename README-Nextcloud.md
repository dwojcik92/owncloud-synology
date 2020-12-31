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


# Tutorial Apache - Enable HTTPS

Install the Apache server and the required packages.
```
apt-get update

apt-get install apache2 openssl
```

Enable Apache module named: Mod_ssl.

Enable Apache module named: Mod_rewrite.
```
a2enmod ssl
a2enmod rewrite
```

Edit the Apache configuration file.
```
vi /etc/apache2/apache2.conf
```

Add the following lines at the end of this file.

```
<Directory /var/www/html>
    AllowOverride All
</Directory>
```

Create a private key and the website certificate using the OpenSSL command.

```
mkdir /etc/apache2/certificate
cd /etc/apache2/certificate
openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out apache-certificate.crt -keyout apache.key
```

Enter the requested information.

On the option named COMMON_NAME, you need to enter the IP address or hostname.

In our example, we used the IP address 200.200.200.2000.

Edit the Apache configuration file for the default website.

```
vi /etc/apache2/sites-enabled/000-default.conf
```

Here is the file, before our configuration.

```
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Here is the file, after our configuration.
```
<VirtualHost *:443>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
        SSLEngine on
        SSLCertificateFile /etc/apache2/certificate/apache-certificate.crt
        SSLCertificateKeyFile /etc/apache2/certificate/apache.key
</VirtualHost>
```
Optionally, you may want to redirect HTTP users to the HTTPS version of your website.

In this case, use the following configuration.
```
<VirtualHost *:80>
        RewriteEngine On
        RewriteCond %{HTTPS} !=on
        RewriteRule ^/?(.*) https://%{SERVER_NAME}/$1 [R=301,L]
</virtualhost>

<VirtualHost *:443>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
        SSLEngine on
        SSLCertificateFile /etc/apache2/certificate/apache-certificate.crt
        SSLCertificateKeyFile /etc/apache2/certificate/apache.key
</VirtualHost>
```

Restart the Apache service.
```
service apache2 restart
```

Open your browser and access the HTTPS version of your website.

In our example, the following URL was entered in the Browser:

• https://200.200.200.200

The Apache server will display the HTTPS version of your website.
