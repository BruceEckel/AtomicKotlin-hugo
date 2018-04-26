@echo off
hugo
py -3 deploy.py
cd ..\AtomicKotlin.github.io
@echo on
git commit -a -m "update"
git push
cd ..\AtomicKotlin-hugo
