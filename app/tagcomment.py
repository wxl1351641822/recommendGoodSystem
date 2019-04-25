#!/usr/bin/env python
# -*-coding:utf-8-*-
import random
import math
from app import sql


class recommend():
    user_tags = dict();
    tag_items = dict();
    user_items = dict();
    user_items_test = dict();  # 测试集数据字典
    item_tags = dict()  # 用于多样性测试
    # 统计各类数量
    def addValueToMat(self,theMat, key, value, incr):
        if key not in theMat:  # 如果key没出先在theMat中
            theMat[key] = dict();
            theMat[key][value] = incr;
        else:
            if value not in theMat[key]:
                theMat[key][value] = incr;
            else:
                theMat[key][value] += incr;  # 若有值，则递增





    # 初始化，进行各种统计
    def InitStat(self):
        sqlstr="select * from recommend_tag"
        re_tag=sql.select(sqlstr)
        print(re_tag)
        if(re_tag['error']==0):
            for data in re_tag['data']:
                user = str(data['userid']);
                item = data['goodid'];
                tag = data['tag'];
                if random.random() > 0.1:  # 将90%的数据作为训练集，剩下10%的数据作为测试集
                    self.addValueToMat(self.user_tags, user, tag, 1)
                    self.addValueToMat(self.tag_items, tag, item, 1)
                    self.addValueToMat(self.user_items, user, item, 1)
                    self.addValueToMat(self.item_tags, item, tag, 1)
                else:
                    self.addValueToMat(self.user_items_test, user, item, 1)
        print("user_tags",self.user_tags)
        print("tag_items", self.tag_items)
        print("user_items", self.user_items)
        print("item_tags", self.item_tags)
        print("user_items_test", self.user_items_test)
        # data_file = open('delicious.dat')
        # line = data_file.readline();
        # while line:
        #     if random.random() > 0.1:  # 将90%的数据作为训练集，剩下10%的数据作为测试集
        #         terms = line.split("\t");  # 训练集的数据结构是[user, item, tag]形式
        #         user = terms[0];
        #         item = terms[1];
        #         tag = terms[2];
        #         addValueToMat(user_tags, user, tag, 1)
        #         addValueToMat(tag_items, tag, item, 1)
        #         addValueToMat(user_items, user, item, 1)
        #         addValueToMat(item_tags, item, tag, 1)
        #         line = data_file.readline();
        #     else:
        #         addValueToMat(user_items_test, user, item, 1)
        # data_file.close();



    # 推荐算法
    def Recommend(self,usr):
        recommend_list = dict();
        tagged_item = self.user_items[usr];  # 得到该用户所有推荐过的物品
        for tag_, wut in self.user_tags[usr].items():  # 用户打过的标签及次数
            for item_, wit in self.tag_items[tag_].items():  # 物品被打过的标签及被打过的次数
                # print(item_,wut,wit)
                if item_ not in tagged_item:  # 已经推荐过的不再推荐
                    if item_ not in recommend_list:
                        recommend_list[item_] = wut * wit;  # 根据公式
                    else:
                        recommend_list[item_] += wut * wit;
        # print(recommend_list)
        return sorted(recommend_list.items(), key=lambda a: a[1], reverse=True)


    # 统计标签流行度
    def TagPopularity(self):
        tagfreq = {}
        for user in self.user_tags.keys():
            for tag in self.user_tags[user].keys():
                if tag not in tagfreq:
                    tagfreq[tag] = 1
                else:
                    tagfreq[tag] += 1
        return sorted(tagfreq.items(), key=lambda a: a[1], reverse=True)


    # 计算标签的余弦相似度
    def CosineSim(self,item_tags, i, j):
        ret = 0
        for b, wib in item_tags[i].items():  # 求物品i,j的标签交集数目
            if b in item_tags[j]:
                ret += wib * item_tags[j][b]
        ni = 0
        nj = 0
        for b, w in item_tags[i].items():  # 统计 i 的标签数目
            ni += w * w
        for b, w in item_tags[j].items():  # 统计 j 的标签数目
            nj += w * w
        if ret == 0:
            return 0
        return ret / math.sqrt(ni * nj)  # 返回余弦值


    # 计算推荐列表多样性
    def Diversity(self,item_tags, recommend_items):
        ret = 0
        n = 0
        for i in dict(recommend_items).keys():
            for j in dict(recommend_items).keys():
                if i == j:
                    continue
                ret += self.CosineSim(item_tags, i, j)
                n += 1
        return ret / (n * 1.0)

    def Test(self):
        self.InitStat()
        recommend_list = self.Recommend("20")
        # print recommend_list
        print(len(recommend_list))
        k=0
        for recommend in recommend_list:  # 兴趣度最高的十个itemid
            # print(recommend[0])
            try:
                print(self.user_items_test['20'][recommend[0]])
                k=k+1
            except Exception as e:
                print(e)
        print(k/len(recommend_list))
        # 标签流行度统计
        tagFreq = self.TagPopularity()
        for tag in tagFreq[:20]:
            print(tag)

        # 推荐列表多样性,计算时间较长
        diversityNum = self.Diversity(self.item_tags, recommend_list)
        print(diversityNum)

r=recommend();
r.Test()