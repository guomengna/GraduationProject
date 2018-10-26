# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import xlrd
import xlwt
G = nx.Graph()
ExcelFile = xlrd.open_workbook('cernet2_added.xlsx','r')
#sheet1 = ExcelFile.sheet_names()
nums = len(ExcelFile.sheets())
for i in range(nums):
    #根据sheet顺序打开sheet
    sheet1 = ExcelFile.sheets()[i]
nrows = sheet1.nrows   #行
ncols = sheet1.ncols   #列
print(nrows,ncols)

#循环行列表数据
for i in range(nrows):
    #print(sheet1.row_values(i))
    list = sheet1.row_values(i)
    list1 = [str(j) for j in list]
    #print(int(list[0]), int(list[1]))
    #print(list1[0], list1[1])
    #print(int(list[0]),int(list[1]))
    G.add_node(int(list[0]))
    G.add_node(int(list[1]))
    #G.add_edge(list[0],list[1])
    #添加带有权值的边
    G.add_weighted_edges_from([(list[0], list[1], list[8])])
    #获取边的权值
    print(G.get_edge_data(list[0], list[1]))

plt.figure()
nx.draw(G, node_color='r', with_labels=True, node_size=800, font_color='w')
plt.show()
