Readme
=====

To set up a new blog publishing arrangement:

```
workon pelican;
mkdir blog;
cd blog;
git clone -b content_only --single-branch git@github.com:theodox/theodox.github.io.git source;
git clone --recursive git@github.com:theodox/pelican-plugins.git;
pip install beautifulsoup4;
pip install webassets;
pip install markdown
```