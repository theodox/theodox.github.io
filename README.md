Readme
=====

To set up a new blog publishing arrangement:

```
mkdir blog;
cd blog;
git clone -b master --single-branch git@github.com:theodox/theodox.github.io.git production;
git github.com:theodox/blog_source.git source;
git clone --recursive git@github.com:theodox/pelican-plugins.git;
git clone --recursive git@github.com:theodox/pelican-themes.git;
```