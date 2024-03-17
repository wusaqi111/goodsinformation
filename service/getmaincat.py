from utils import dbUtil

def get_maincat():
    maincatlist=[]
    dic={}
    db = dbUtil()
    sql1='select category from goods_subkey group by category;'
    # sql2='select subkeycat from goods_subkey where category={0} group by subkeycat;'.format()
    res = db.query(sql1)
    for i in res:
        maincatlist.append(i[0])
    for ii in range(len(maincatlist)):
        dic[maincatlist[ii]]=[]
        sql2="select subkeycat from goods_subkey where category='"+ maincatlist[ii] +"'group by subkeycat;"
        # print(sql2)
        res1 = db.query(sql2)
        dic[maincatlist[ii]] += res1
    db.close()

    # print(dic)
    return dic
if __name__ == '__main__':
    print(get_maincat())
    # print(maincatlist)