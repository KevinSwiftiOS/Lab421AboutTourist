from ..initViews import *;
from django.shortcuts import render;
import json
def singlejq(request):
 if request.is_ajax():
    #景区名是否合法


    param =  json.loads((request.POST.get('param')));

    choosetime = param["time"];
    name = param["name"];
    if len(name)>=5:
        newname=name[0:5]
    else:
        newname=name

    #获取值
    year =   name = param["year"];
    month =  name = param["month"];

    message = [];
    list1 = [];
    list2 = [];
    date = []

    haoping = []
    zhongping = []
    chaping = []
    success = 0;
    finalParam = {};

    jingqu_name = jingqu.get_all_name();
    for i in range(0,len(jingqu_name)):
        if newname == jingqu_name[i]:
            success = 1;
            break;
    if(success):
     if choosetime == 'yue':
        dict1 = jingqu.get_month()
        list1 = dict1[newname][0]
        list2 = dict1[newname][1]

     elif choosetime == 'zhou':
        dict1 = jingqu.get_week()
        list1 = dict1[newname][0]
        list2 = dict1[newname][1]
     elif choosetime == 'tian':
        dict1 = jingqu.get_day()
        list1 = dict1[newname][0][-15:]  # 只取最近15天的数据
        list2 = dict1[newname][1][-15:]
     elif choosetime == 'nian':
        dict1 = jingqu.get_year()
        list1 = dict1[newname][0]
        list2 = dict1[newname][1]
     dict2, dict3 = jingqu.get_message()
     list3 = dict2[newname]
     list4 = dict3[newname];


     message = dict(zip(list4,list3)) #将对应的打包成元祖
     dict4 = jingqu.get_score_message()
     list5 = sorted(dict4[newname].items(),key=lambda d:d[0])
     for i,j in enumerate(list5): #进行遍历对象
        if j[0][0:4]==year and j[0][5:7]==month:
            date.append(j[0])
            j[1].setdefault('差评',0)
            j[1].setdefault('中评',0)
            j[1].setdefault('好评',0)
            haoping.append(j[1]['好评'])
            zhongping.append(j[1]['中评'])
            chaping.append(j[1]['差评'])

     param = {
         "success":success,
        "list1":list1,
        "list2":list2,
        "date":date,
        "chaping":chaping,
        "zhongping":zhongping,
        "haoping":haoping,
        "message":message,
    };
     finalParam = eval(repr(param)); #repr 将数字 列表转化为字符串 eval将字符串类型转化为字典
    else:
        param = {
            "success": success,

        };
    return JsonResponse(finalParam);
 else:
    return render(request, 'singlejq.html');