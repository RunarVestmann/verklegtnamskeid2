Verklegt námskeið 2

Eggert, Guðmundur og Rúnar

#Captain Console, a retro gaming shop like none other!

This repository contains the web solution for Captain Console's online shop.

##Installation guide

```bash
git clone https://github.com/RunarVestmann/verklegtnamskeid2.git
```

```bash
cd verklegtnamskeid2
```

```bash
pip install virtualenv
```

```bash
cd captain_console
```

```bash
virtualenv -p python venv
```

Windows:
```bash
source venv/Scripts/activate
```

Mac:
```bash
source venv/bin/activate
```

```bash
pip install -r ../requirements.txt
```

```bash
python manage.py runserver
```

Now the server should be responding to http://127.0.0.1:8000/