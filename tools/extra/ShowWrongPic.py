# coding: utf-8
import sys
import numpy as np
import re
import struct
import matplotlib.pyplot as plt

def get_wrong_num():
    bachSize = 100
    flag = 0 #第一次读取到错误样本的数据标记，如果flag=0，表示没有错误数据，flag=1表示有错误数据
    countNum = 0 #countNum=0表示没有序号需要修正，countNum=1表示有序号需要修正
    #read file
    for line in open("/home/ly/caffe/Log/caffe.bin.INFO"):
        outer_num_str = re.findall(r"outer_num_ \d+", line)
        predict_num_str = re.findall(r"predict_num \d+", line)
        label_value_str = re.findall(r"label_value \d+", line)
        if len(outer_num_str) == 0 and countNum == 0:
            continue
        elif len(outer_num_str) != 0 and flag == 0: #首次找到错误信息
            flag = 1
            countNum += 1
            outer_num_ = int(re.findall(r"\d+", outer_num_str[0])[0])
            predict_num = int(re.findall(r"\d+", predict_num_str[0])[0])
            label_value = int(re.findall(r"\d+", label_value_str[0])[0])
            line_num_info = np.array([[outer_num_, predict_num, label_value]])
            wrong_num_info = line_num_info.copy()
            continue
        elif len(outer_num_str) != 0:
            countNum += 1
            outer_num_ = int(re.findall(r"\d+", outer_num_str[0])[0])
            predict_num = int(re.findall(r"\d+", predict_num_str[0])[0])
            label_value = int(re.findall(r"\d+", label_value_str[0])[0])
            line_num_info = np.array([[outer_num_, predict_num, label_value]])
            wrong_num_info = np.r_[wrong_num_info, line_num_info]
            continue
        bach_str = re.findall(r"Batch? \d+", line)
        bach_num = int(re.findall(r"\d+", bach_str[0])[0])
        offset = bach_num * bachSize
        for i in range(wrong_num_info.shape[0]-countNum, wrong_num_info.shape[0]):
            wrong_num_info[i,0] += offset
        countNum = 0
    return wrong_num_info

def showMnist(wrong_num_info):
    print wrong_num_info

    filename = '/home/ly/caffe/data/mnist/t10k-images-idx3-ubyte'
    binfile = open(filename , 'rb')
    buf = binfile.read()

    headerSize = 0
    magic, numImages , numRows , numColumns = struct.unpack_from('>IIII' , buf , headerSize)
    headerSize += struct.calcsize('>IIII') #跳过前面的 magic, numImages, numRows, numColumns

    for idx, val in enumerate(wrong_num_info):
        index = headerSize
        index += (val[0] * struct.calcsize('>784B'))
        im = struct.unpack_from('>784B', buf, index)

        im = np.array(im)
        im = im.reshape(28,28)

        fig = plt.figure(figsize=(9,9),dpi=10)
        plotwindow = fig.add_subplot(111)
        plt.title(str(wrong_num_info[idx,2]) + "->" + str(wrong_num_info[idx,1]),fontsize=100)
        plt.imshow(im , cmap='gray')
        plt.show()


if __name__ == "__main__":
    wrong_num_info = get_wrong_num()
    showMnist(wrong_num_info)
