uid_score_bid=['A,1,a','A,1,b','A,1,d','B,1,b','B,1,c','B,1,e','C,1,c','C,1,d','D,1,b','E,1,a','E,1,d'];

#基于物品的协同过滤
from math import sqrt,pow
import operator

#1.构建用户-->物品的倒排
def loadData(files):
    data={};
    for line in files:
        user , score, item = line.split(",");
        data.setdefault(user,{});
        data[user][item]=score;
    print("----1.用户：物品的倒排----")
    print(data)
    return data

#2.计算
# 2.1 构造物品-->物品的共现矩阵
# 2.2 计算物品与物品的相似矩阵
def similarity(data):
    # 2.1构造物品：物品的共现矩阵
    N={}#喜欢物品的总人数
    C={}#喜欢物品i也喜欢j的人数
    for user,item in data.items():
        for i,score in item.items():
            N.setdefault(i,0)
            N[i]+=1;
            C.setdefault(i,{})
            for j,scores in item.items():
                if j not in i:
                    C[i].setdefault(j,0);
                    C[i][j]+=1;
    print("----2.构造的共现矩阵----")
    print('N:',N)
    print('C:',C)

    #2.2计算物品与物品的相似矩阵
    W={}
    for i,item in C.items():
        W.setdefault(i,{})
        for j,item2 in item.items():
            W[i].setdefault(j,0)
            W[i][j]=C[i][j]/sqrt(N[i]*N[j])
    print("----3.构造相似矩阵----")
    print(W)
    return W


def recommandList(data,W,user,k=3,N=10):
    rank={}
    for i,score in data[user].items():#获得用户user历史记录，如A用户的历史记录为{'a': '1', 'b': '1', 'd': '1'}
        for j,w in sorted(W[i].items(),key=operator.itemgetter(1),reverse=True)[0:k]:#获得与物品i相似的k个物品

            if j not in data[user].keys():#该相似的物品不在用户user的记录里
                rank.setdefault(j,0)
                rank[j]+=float(score)*w
    print("---4.推荐----")
    print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:N])
    return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:N];



####################基于用户的协同推荐##############################################################
class UserCf():
#     获得初始化数据
    def __init__(self,data):
        self.data=data;

#     通过用户名获得电影列表
    def getItems(self,username1,username2):
        return self.data[username1],self.data[username2]

#     j计算两个用户的皮尔逊相关系数
    def pearson(self,user1,user2):
        # 数据格式为：电影，评分  {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}
        sumXY=0.0
        n=0;
        sumX=0.0
        sumY=0.0
        sumX2=0.0
        sumY2=0.0
        r=0
        try:
            for movie1,score1 in user1.items():
                if movie1 in user2.keys():
                    n+=1
                    sumXY+=score1*user2[movie1]
                    sumX+=score1
                    sumY+=user2[movie1]
                    sumX2+=pow(score1,2)
                    sumY2+=pow(user2[movie1],2)

            molecule=sumXY-(sumX*sumY)/n

            denominator=sqrt((sumX2-pow(sumX,2)/n)*(sumY2-pow(sumY,2)/n))
            r=molecule/denominator
        except Exception as e:
            import traceback
            print("异常信息：",traceback.print_exc())
        return r

#计算与当前用户的距离，获得最临近的用户
    def nearstUser(self,username,n=1):
        distances={};#用户，相似度
        for otherUser,items in self.data.items():#遍历整个数据集
            if otherUser not in username:#不是当前用户
                distance=self.pearson(self.data[username],self.data[otherUser])#计算两个用户的相似度
                distances[otherUser]=distance
        sortedDistance=sorted(distances.items(),key=operator.itemgetter(1),reverse=True)#最相似的N个用户
        print("排序后的用户为：",sortedDistance)
        return sortedDistance[:n]

#     给用户推荐电影
    def recomand(self,username,n=1):
        recommand={}
        for user,score in dict(self.nearstUser(username,n)).items():
            print("推荐的用户：",(user,score))
            for movies,scores in self.data[user].items():#推荐的用户的电影列表
                if movies not in self.data[username].keys():
                    # 当前username没有看过
                    print("%s为该用户推荐的电影：%s" % (user, movies))
                    if movies not in recommand.keys():  # 添加到推荐列表中
                        recommand[movies] = scores
                return sorted(recommand.items(), key=operator.itemgetter(1), reverse=True);  # 对推荐的结果按照电影评分排序

if __name__=='__main__':
    #用户，兴趣度，物品
    uid_score_bid = ['A,1,a', 'A,1,b', 'A,1,d', 'B,1,b', 'B,1,c', 'B,1,e', 'C,1,c', 'C,1,d', 'D,1,b', 'E,1,a', 'E,1,d'];
    data=loadData(uid_score_bid)
    W=similarity(data)
    recommandList(data, W, 'A', 3, 10);  # 推荐
    users = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                           'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                           'The Night Listener': 3.0},

             'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                              'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                              'You, Me and Dupree': 3.5},

             'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                  'Superman Returns': 3.5, 'The Night Listener': 4.0},

             'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                              'The Night Listener': 4.5, 'Superman Returns': 4.0,
                              'You, Me and Dupree': 2.5},

             'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                              'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                              'You, Me and Dupree': 2.0},

             'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                               'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},

             'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}
             }
    userCf = UserCf(data=users)
    recommandList = userCf.recomand('Toby', 2)
    print("最终推荐：%s" % recommandList)



