`Thweddy` is a web-based helper tool for Twitter, written in Python using the Django framework.

`Thweddy` allows you to group a bunch of tweets into a single conversation thread, and then refer to a unique Thweddy URL to link back to (e.g. to show a conversation on Twitter to other friends).

To make creating threads as easy as possible `Thweddy` has a reverse look up feature that will attempt to resolve a thread of tweets backwards from the last one in the conversation (unfortunately going forward from the first tweet won't work as the Twitter API currently doesn't support this; also please not that some tweets may not have the current IDs to do this look up).

Installation and Setup
======================

Requirements
    django

    tweepy

    blueprint-css

    django-dynamic-formset

Optional
    memcached (or some other caching backend)

To install with git::

    git clone git://github.com/1stvamp/thweddy.git
    cd thweddy
    git submodule update --init
    source env.sh
    cp thweddy/settings-dist.py thweddy/settings.py
    cp thweddy/main/twitter/settings-dist.py thweddy/main/twitter/settings.py
    python thweddy/manage.py syncdb
    # See below for instructions on configuring settings and twitter settings

To install from tar::

    wget http://github.com/1stvamp/thweddy/tarball/master
    tar xzf 1stvamp-thweddy-*.tar.gz
    mv 1stvamp-thweddy-*/ thweddy/
    cd thweddy
    source env.sh
    rm -rf django tweepy thweddy/static/css/blueprint-css thweddy/static/js/django-dynamic-formset
    wget http://github.com/django/django/tarball/17ed5ce726ed716165a0d30b79692f6c6d0c6a33
    tar xzf django-django*.tar.gz
    mv django-django*/ django/
    wget http://github.com/joshthecoder/tweepy/tarball/45d5a4ac44aac2b0023239bcc5c1100ab4a6fcb1
    tar xzf joshthecoder-tweepy*.tar.gz
    mv joshthecoder-tweepy*/ tweepy/
    cd thweddy/static/css
    wget http://github.com/joshuaclayton/blueprint-css/tarball/2e3e4f59cfcd8265059a063a4a2a8508b6f9f46c
    tar xzf joshuaclayton-blueprint-css*.tar.gz
    mv joshuaclayton-blueprint-css*/ blueprint-css/
    cd ../js
    wget http://github.com/1stvamp/django-dynamic-formset/tarball/9993366028e06e7407eaf5fea268119e43df77d6
    tar xzf 1stvamp-django-dynamic-formset*.tar.gz
    mv 1stvamp-django-dynamic-formset*/ django-dynamic-formset/
    cd ../../../
    cp thweddy/settings-dist.py thweddy/settings.py
    cp thweddy/main/twitter/settings-dist.py thweddy/main/twitter/settings.py
    python thweddy/manage.py syncdb
    # See below for instructions on configuring settings and twitter settings

Configuration
=============

If you followed either of the steps above you should have a distribution version of `Thweddy` ready to go.
Before you can run it, you need to edit ``thweddy/settings.py`` and ``thweddy/main/twitter/settings.py`` with your config info.

    SECRET_KEY
        Intentionally left blank so you _have_ to put something here. This is used for hashing passwords and needs to be unique and secure (e.g. don't give it out). For something fairly strong I'd suggest running ``dd if=/dev/urandom count=1 | tr -cd 'A-Za-z0-9!"%^^&*()@~#?\/<>.,' | cut -c1-50; echo`` in a terminal and using the first line of the output as your secret key.
    
    DEBUG
        Does what it says on the tin, if something fails you'll get a nice traceback etc., but this should be set to ``False`` on any production deployment.

    DATABASE_*
        Your database connection details, see the Django docs for detailed info, but `Thweddy` needs a DB to work. If you can't be bothered with anything complex _and_ it's not going to be heavily used, just set DATABASE_ENGINE to sqlite3 and DATABASE_NAME to a file path with other DATABASE_* options left as a blank string.

    ADMIN_URL
        As an added optional security feature (well, security through partial obscurity anyway) you can set your Django admin URL to a custom address (e.g. ``r'^my_secret_admin_site/'`` instead of ``r'^admin/'``), to minimise any attacks due to people automatically scanning for ``/admin/``.

Twitter configuration
=====================

    CONSUMER_KEY
        oAuth Twitter consumer key, see http://apiwiki.twitter.com/OAuth-FAQ.
    CONSUMER_SECRET
        oAuth consumer secret, see http://apiwiki.twitter.com/OAuth-FAQ.
    CALLBACK_URL
        URL Twitter will (hopefully) redirect back to after authenticating the user.
    ANON_USER
        Username to connect to Twitter with using basic auth for API access when oAuth isn't available.
    ANON_PASS
        Password to connect to Twitter with using basic auth for API access when oAuth isn't available.


