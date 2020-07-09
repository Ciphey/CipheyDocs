# CipheyDocs
Documentation for Ciphey

Papers is for the papers we've written.
Docs is where we build the Sphinx docs.

# Making DocStrings builds
Use Sphinx-apidoc
```
➜ sphinx-apidoc /home/bee/.local/lib/python3.8/site-packages/ciphey -o .
```

where the first argument is the location of the Ciphey install, the -o is the output. Build in /docs

# To build
Run `nox` in the root directory.

