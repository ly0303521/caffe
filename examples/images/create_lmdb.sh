# /usr/bin/env sh
DATA=examples/images
rm -rf $DATA/img_MyTest_lmdb
build/tools/convert_imageset --gray --shuffle --resize_height=28 --resize_width=28 \
--encode_type=png \
/home/ly/caffe/examples/images/ $DATA/FileList.txt  $DATA/img_MyTest_lmdb
