# /usr/bin/env sh
DATA=examples/images
echo "Create FileList.txt..."
rm -rf $DATA/FileList.txt
find $DATA -name *.png | cut -d '/' -f3 | sed "s/$/ 1/">>$DATA/FileList.txt
#find $DATA -name *bike.jpg | cut -d '/' -f3 | sed "s/$/ 2/">>$DATA/tmp.txt
#cat $DATA/tmp.txt>>$DATA/FileList.txt
#rm -rf $DATA/tmp.txt
echo "Done.."
