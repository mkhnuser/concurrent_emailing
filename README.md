# Concurrent emailing

## Overview

Simple package that allows concurrent email sending. Each email is sent within a separate thread.

## Example of usage

<pre>
# bash
export SMTP_SERVER_HOST="smtp.gmail.com"
export SMTP_SERVER_PORT="465"
export EMAIL_ADDRESS="address@email.com"
export EMAIL_PASSWORD="password"
python -m concurrent_emailing
</pre>
```SMTP_SERVER_HOST``` and ```SMTP_SERVER_PORT``` are used to identify SMTP server;
<br>```EMAIL_ADDRESS``` and ```EMAIL_PASSWORD``` are credentials for an email from which *emails* will be sent. ```data.csv``` file is used to get email data by default.

During package invocation a number of optional arguments are available. Consult source code for more information.

## Notes

- Argument parser is defined in a global scope, prior to anything else, to emphisize that one is used both when the script is executed as ```__main__``` and when the script is imported (consult ```__main__.py``` file). Moreover, such a technique always displays parser's help command even if exception is raised later on.
- Environment variables are explicitly converted. That is, if they are not specified or they have wrong type, exception is raised.
