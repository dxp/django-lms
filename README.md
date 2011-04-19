ID Intranet (needs a better name)
=================================

After ten years of use, we are looking to replace our old intranet here at ID (www.id.iit.edu). There are many options out there, but almost all of them are too heavy weight for us. Being a Django shop, we looked for a Django course management / intranet system. Couldn't find one. That is where this project was born.

It aims to be a simple system. Starting with a springborad interface that is easily customizable from Django's admin. It will include a few modules by default: classes, people, news & alerts, admin, help, and knowledge base.

If you're interested in helping, please drop me a line at cezar@id.iit.edu

Installation
------------

The settings files included I've setup using the [layout](http://blog.zacharyvoase.com/2010/02/03/django-project-conventions/) suggested by Zachary Voase.

    SITE_ROOT/
    |-- bin/      # Part of the virtualenv
    |-- cache/    # A filesystem-based cache
    |-- db/       # Store SQLite files in here (during development)
    |-- include/  # Part of the virtualenv
    |-- lib/      # Part of the virtualenv
    |-- log/      # Log files
    |-- pid/      # PID files
    |-- share/    # Part of the virtualenv
    |-- sock/     # UNIX socket files
    |-- tmp/      # Temporary files
    `-- uploads/  # Site uploads
