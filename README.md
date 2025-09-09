# ToDo-List-app

ToDo List app integration for Slack's Slash commands

The webapp is access  Django end point when start the sever  


This webapp contains three apis, namely
- https://b5616c2ab2a4.ngrok-free.app/api/task-add/
- https://b5616c2ab2a4.ngrok-free.app/api/task-list/
- https://b5616c2ab2a4.ngrok-free.app/api/task-remove/

These three apis are integrated with three slash commands of slack

/addtodo  ->  https://b5616c2ab2a4.ngrok-free.app/api/task-add/
/listtodo  -> https://b5616c2ab2a4.ngrok-free.ap/api/task-list/
/marktodo  -> https://b5616c2ab2a4.ngrok-free.ap/api/task-remove/

To run the project:-

1. Fork the repo.
2. Clone and download it.
3. Install Python, version=3.5.2
4. Run the command 
- pip install virtualenv
- cd ~/../project-directory
- virtualenv .
- source ../bin/activate (for MacOS and Linux)
- pip install -r requirements.txt
- python manage.py migrate
- On the terminal, type the following command and provide username, password and email for the admin user
```bash
$ python manage.py createsuperuser
```

That was pretty simple, right? Now let's make the App live. We just need to start the server now and then we can start using our simple todo App. Start the server by following command
- python manage.py runserver 8000
- python manage.py runserver 0.0.0.0:8000

Now the following 3 urls can be accessed using localhost:8000 domain

from outside your local network, Django’s dev server won’t allow it by default, because:

    Dev server is not designed for public internet exposure
    It binds to an IP (e.g., LAN IP or hostname) and isn’t hardened for security.

    Port 8000 isn’t open to the outside world
    Your router/firewall likely blocks inbound requests from the internet.

     If you just need public testing temporarily

Use ngrok or similar tunneling service:

     pip install pyngrok
      ngrok http 8000

It will give you a public HTTPS URL like:

https://abcd1234.ngrok-free.app/api/task-list/

and forward it to your Django dev server.
