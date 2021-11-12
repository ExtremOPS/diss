#!/bin/bash
clear
git latexdiff --version > /dev/null
RET=$?
# if [ $RET -ne 0 ]; then echo -e "\nInstall git latexdiff using: git clone https://gitlab.com/git-latexdiff/git-latexdiff\n"; exit $RET;
# fi

echo -e "git latexdiff from https://gitlab.com/git-latexdiff/git-latexdiff\n"

if [ "$#" -eq 0 ]; then
  echo -e "Usage:" >&2
  echo -e "\tCompare FILENAME HEAD~1 to HEAD" >&2
  echo -e "\t\t\t $0 FILENAME" >&2
  echo -e "\tCompare FILENAME OLD_COMMIT to HEAD" >&2
  echo -e "\t\t\t $0 FILENAME OLD_COMMIT" >&2
  echo -e "\tCompare FILENAME OLD_COMMIT to NEW_COMMIT" >&2
  echo -e "\t\t\t $0 FILENAME OLD_COMMIT NEW_COMMIT" >&2
  exit -1
elif [ "$#" -eq 1 ]; then 
    FILENAME=$1    
    OLD_COMMIT_ID="HEAD~1"
    NEW_COMMIT_ID="HEAD"
elif [ "$#" -eq 2 ]; then 
    FILENAME=$1    
    OLD_COMMIT_ID=$2
    NEW_COMMIT_ID="HEAD"
else 
    FILENAME=$1   
    OLD_COMMIT_ID=$2
    NEW_COMMIT_ID=$3
fi

OPTIONS="--flatten --latexmk --cleanup keeppdf --no-view --whole-tree"
# OPTIONS="$OPTIONS -V "
# OPTIONS="$OPTIONS -V"
# OPTIONS="$OPTIONS --biber"
OPTIONS="$OPTIONS --disable-citation-markup"
# OPTIONS="$OPTIONS --exclude-safecmd=\"svgwidth\""
# OPTIONS="$OPTIONS -c \"FLOATENV=(?:figure|figure*|subfigure|table|plate)[\w\d*@]*\""
# OPTIONS="$OPTIONS -c \"PICTUREENV=(?:picture|DIFnomarkup|tabular|tikzpicture)[\w\d*@]*\""
# --exclude-textcmd=\"cite,subfigure,subfigure*,equation,align,figure,figure*,label\"" 
# OPTIONS="$OPTIONS --exclude-textcmd=\"SI\""
OPTIONS="$OPTIONS --exclude-safecmd=\"cite,cref,Cref,label\""
OPTIONS="$OPTIONS --append-mboxsafecmd=\"SI,addplot\""
OPTIONS="$OPTIONS --tmpdirprefix $PWD"
OPTIONS="$OPTIONS -o diff_$FILENAME.pdf"
OPTIONS="$OPTIONS --main $FILENAME.tex"
#echo $OPTIONS

#get id of the last commit
#PREVIOUS_COMMIT_ID=`git log --skip 1 -n 1 --oneline --no-abbrev-commit | awk '{print $1}'`
echo "The options are"
echo $OPTIONS
echo ""
echo -e "Comparing commit $NEW_COMMIT_ID with the $OLD_COMMIT_ID of file 
$FILENAME.tex\n"
echo "Starting git-latexdiff"
echo "Please be patient..."
git latexdiff --prepare 'python3 10_Figures/ConvertAndFix.py' $OPTIONS $OLD_COMMIT_ID $NEW_COMMIT_ID
perl -pne 's/\\SI\{(.*?)}{(.*?)\}/\\mbox{\\SI{$1}{$2}}/g' git-latexdiff*/new/$FILENAME.tex > new-mod.tex
mv new-mod.tex git-latexdiff*/new/$FILENAME.tex
latexmk -pdf git-latexdiff*/new/$FILENAME.tex -outdir=./compile/
mv compile/$FILENAME.pdf diff_$FILENAME.pdf
rm -rf git-latexdiff*
rm -rf compile
# git latexdiff $OPTIONS $OLD_COMMIT_ID $NEW_COMMIT_ID
