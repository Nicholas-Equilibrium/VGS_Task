# VGS_Task
 
Utilizes Docker image from example project listed in task description.
- Because nginx and gunicorn don't play well with windows. 

Set up is relativly simple

You will need to install two pieces of software <br>
:: Docker<br>
:: Ngrok

Open Ngrok and type ngrok.exe http 8000<br>
Copy: Subdomain<br>
Example: `https://234lsk2l35kk35.ngrok.io`

Open: docker-compose.yml<br>
Change: DJANGO_APP_URL="your ngrok subdomain"<br>
Example: DJANGO_APP_URL=`https://7a0e6326510d.ngrok.io`<br>
Change: INBOUND_ROUTE="your vgs inbound route url"<br>
Example: INBOUND_ROUTE=`https://tntqdfnpdme.sandbox.verygoodproxy.com`<br>

Open: /first/settings.py<br>
Change: ALLOWED_HOSTS = ['localhost', '.verygoodproxy.com', 'your ngrok url here']<br>
Example: ALLOWED_HOSTS = ['localhost', '.verygoodproxy.com', `'7a0e6326510d.ngrok.io'`]<br>
Change: OUTBOUND_ROUTE = "your vgs outbound route"<br>
Example: OUTBOUND_ROUTE =`'https://US6CVysgkj4DFGDGsdf:d33acfb6-06fa-33fs-867b-dd8f2f6f4c63@tntq8dnpdme.sandbox.verygoodproxy.com:8080'`


Finally configure vgs routes according to readme inside of /Task/

Run "rerun.sh"

Open up web browser and type 127.0.0.1:8001