Data validation

Z FE mu to nabizi jenom data koncici na .csv. V Pripade ze pretahne mam be posefenej.
Pripady kdy : neuploadne zadny soubory, proloopuje vsechny soubory a pokud nejsou contenttype text/csv nebo nekončí na .csv. Dale take kontroluje pokud bude chybet nejak hlavička nebo neco v ni. A na konci pokud to nebude ani jedno z toho vypise se genericka zprava erroru. V pripade ze prvni hlavicka bude ok a ostatni nebudou tak se to stejne provede protze to pouziva tu prvni hlavicku soboru. 
Ani file size limit ze strany fe

BE - validate_email, env (decouple) stope sensitive niformation
checking for .csv



Zabezpeceni

Bylo nutné zabezpecit fe I be
Skrz postmana byla zajisteno. File type a Size validation nebyla, content type val-diaton, CSRF cross site request forgery .env file tajné věci bude použito https, zminim v nasazeni

Content type – malicious uploads, files se scriptem nebo trebaprocesovani file ale bude to obrovskej obrazek
Cross-Site Scripting diky django build in middeleware 
Clickjacking 'django.middleware.security.SecurityMiddleware'

XSS CORS

ou are using FormData to construct a set of key/value pairs representing form fields and their values. This is a common and secure way to handle file uploads. FormData takes care of encoding the form data for you, including the files.
When you send this FormData object in a POST request using the Fetch API, the data is sent as multipart/form-data. This allows you to transmit binary data, such as files, safely.+

CSRF ->csrf_exempt

HTTPS render

The CorsMiddleware is included for handling Cross-Origin Resource Sharing (CORS). X_FRAME_OPTIONS = 'DENY' helps to prevent your site from being embedded in an iframe, protecting against clickjacking attacks.

env napriklad pro schovani django_secret key


BACKEND REALIZACE

ja nepopisuju jak funguje ALE PROCES