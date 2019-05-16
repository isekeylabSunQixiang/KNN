from numpy import *
import operator
import xlrd
import matplotlib.pyplot as plt

def classify(inputPoint,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]     #已知分类的数据集（训练集）的行数
    diffMat = tile(inputPoint,(dataSetSize,1))-dataSet  #样本与训练集的差值矩阵
    sqDiffMat = diffMat ** 2                    #差值矩阵平方
    sqDistances = sqDiffMat.sum(axis=1)         #计算每一行上元素的和
    distances = sqDistances ** 0.5              #开方得到欧拉距离矩阵
    sortedDistIndicies = distances.argsort()    #按distances中元素进行升序排序后得到的对应下标的列表
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0)+1      #按classCount字典的第2个元素（即类别出现的次数）从大到小排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def excel2matrix(excel):
    data = xlrd.open_workbook(excel)
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    dataset = []
    for i in range(0, nrows):
        all_rowdata = table.row_values(i)
        dataset.append([all_rowdata[0], all_rowdata[1]])
    return dataset

if __name__ == "__main__" :
    train_excel = 'D:\\2\\1train.xlsx'
    label_excel = 'D:\\2\\class.xlsx'
    test_excel = 'D:\\2\\1test.xlsx'
    train_dataset = excel2matrix(train_excel)
    train_dataset = array(train_dataset)
    test_dataset = excel2matrix(test_excel)
    print(test_dataset)
    label_data = xlrd.open_workbook(label_excel)
    label_table = label_data.sheets()[0]
    label_nrow = label_table.nrows
    label = []
    for i in range(0, label_nrow):
        all_rowdata = label_table.row_values(i)
        label.append(all_rowdata[0])
    labels = label
    result = []
    k = int(input("请输入k值："))
    for i in range(len(test_dataset)):
        classes = classify(test_dataset[i], train_dataset, labels, k)
        result.append(classes)
    print(result)
    test_dataset = array(test_dataset)
    plt.scatter(train_dataset[:, 0], train_dataset[:, 1], marker="*", c=labels, s=10, label="train_dataSet")
    plt.scatter(test_dataset[:, 0], test_dataset[:, 1], marker=".", c=result, s=90, label='test_dataSet')
    plt.legend(loc="upper left")
    plt.show()


