#! /bin/bash

###############################################################################
#Copyright (C) 2012 Caio Hoffman, caiohoffman [at] gmail [dot] com            #
###############################################################################
#Permission is hereby granted, free of charge, to any person obtaining a copy #
# of this software and associated documentation files (the "Software"), to    #
# deal in the Software without restriction, including without limitation the  #
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or #
# sell copies of the Software, and to permit persons to whom the Software is  #
# furnished to do so, subject to the following conditions:                    #
#                                                                             #
#The above copyright notice and this permission notice shall be included in   #
# all copies or substantial portions of the Software.                         #
#                                                                             #
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS#
# IN THE SOFTWARE.                                                            #
###############################################################################

if [ -z "$1" ];
then
	echo "[Error] Usage: ./build file.tex yes|no [optional flag to use makeindex, default: no]"
	exit
fi

if [ ! -z "$2" ] && [ "" != "$(echo $2 | sed 's/\(yes\|no\)//g')" ];
then
	echo "[Error] Usage: ./build file.tex yes|no [optional flag to use makeindex, default: no]"
	exit
fi

filename=`echo "$1" | sed 's/\.[tT]\?[eE]\?[xX]\?//'`
tex=$filename".tex"

#pdflatex -interaction=nonstopmode %.tex|bibtex %.aux|makeindex -s %.ist -t %.glg -o %.gls %.glo|pdflatex -interaction=nonstopmode %.tex|pdflatex -interaction=nonstopmode %.tex

echo "Compiling..."
echo ""
pdflatex="pdflatex -interaction=nonstopmode -shell-escape $tex"
echo "$pdflatex"
eval "$pdflatex" 1> texer.out 2> texer.err
thereisbib=$(grep -nH '\\printbibliography' "$tex")
if [ ! -z "$thereisbib" ];
then
	bibtex="biber $filename"
	echo "$bibtex" 
	eval "$bibtex" 1>> texer.out 2>> texer.err
fi;
if [ "yes" == "$(echo $2)" ];
then
	makeglossaries="makeindex -s \"$filename.ist\" -t \"$filename.glg\" -o \"$filename.gls\" \"$filename.glo\""
	echo "$makeglossaries"
	eval "$makeglossaries" 1>> texer.out 2>> texer.err
	makeindex="makeindex \"$filename.idx\""
	echo "$makeindex"
	eval "$makeindex" 1>> texer.out 2>> texer.err
fi
echo "$pdflatex"
eval "$pdflatex" 1>> texer.out 2>> texer.err
echo "$pdflatex"
eval "$pdflatex" 1>> texer.out 2>> texer.err
echo ""
echo "Finished!"

err=`cat texer.out | grep '[eE][rR][rR][oO][rR]'`
if [ ! -z "$err" ];
then
	echo "There would be errors, please check."
else
	err=`cat texer.err|grep '[eE][rR][rR][oO][rR]'`
	if [ ! -z "$err" ];
	then
		echo "There would be errors, please check."
	fi
fi
