## Getting started
<hr>
<p> To make contibution on the website please go through the following steps</p>

<!-- 1. Fork this repository. -->

1. Clone this repository to your local machine:

```bash
    git clone https://github.com/techhub-community/csoc_platform.git
    cd csoc_platform
```

2. Create a virtual enviornment:

```bash
    python3 -m venv env_name
```

- On Mac/Linux

```bash
    source env_name/bin/activate
```

- On Windows

```bash
    env_name\Scripts\activate
```

3. Install requirements

```bash
    pip install -r requirements.txt
```

4. Shell Script Permissions and Execution

```bash
    chmod +xwr run_local.sh
    chmod +xwr run_migrations.sh
    chmod +xwr run_commands.sh
```

```bash
    ./run_local.sh
    ./run_migrations.sh
```

5. Run Project

```bash
    ./run_commands.sh runserver
```

6. Add .env file to the root directory

It's content should be 
```
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=True
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=465
EMAIL_HOST_USER=YOUR_EMAIL_ID
EMAIL_HOST_PASSWORD=YOUR_APP_PASSWORD_FOR_EMAIL
DEFAULT_FROM_EMAIL=YOUR_EMAIL_ID
EMAIL_USE_SSL=True
```