## Delta/notebook

```
sudo -H pip3 install jupyter
sudo -H pip3 install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
jupyter nbextension enable python-markdown/main
jupyter notebook --no-browser

jupyter nbconvert --to html burrows.ipynb
```

### Install IRkernel
```
install.packages('IRkernel')
IRkernel::installspec()
```
This has to be done from Terminal, not R or RStudio.

This will need to be redone the week of 27 April, after the release
of R 4.0.0.
