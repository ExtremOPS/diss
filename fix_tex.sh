#!/bin/bash
pwd
perl -pne 's/\\SI\{(.*?)}{(.*?)\}/\\mbox{\\SI{$1}{$2}}/g' main.tex > new.tex
mv new.tex main.tex
