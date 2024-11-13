#!/bin/bash

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

export IFS=`echo -ne '\n\r'`

echo -e "\033[34;31mThis script can bring problems. Be sure about what you're doing. Close the DropBox for safety.\033[0m"

FILES=$(find -name '*.???~' && find -name '*.???' && find -name '*.backup')
FILES=$(echo "$FILES" | egrep -v '(.tex$|.sty$|.bib$|.png$|.jpg$|.ods$|.pdf$|.eps$|.bmp$|.gif|.cls|.ppt|.doc|.xls|.csv|.svn|.txt$|.git|.xcf)')

echo ""
echo -e "\033[40;41mFiles to be erased:\033[0m"
echo ""

echo "$FILES"

echo ""
echo ""
echo "If you are sure about excluding this files please type yes, otherwise anything to exit."
printf "[yes/no]: "; read ANSWER;
echo ""

if [ "yes" == "$(echo $ANSWER)" ];
then
	if [ -n "$FILES" ]
	then
		rm $FILES
		echo "Extra files have gone."
	else
		echo "There is no extra files."
	fi
else
	echo "No file was removed."	
fi

#END
