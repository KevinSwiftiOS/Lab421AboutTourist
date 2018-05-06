

from ..initViews import jingqu;
from django.shortcuts import render;
import json
def singlejq(request):
    choosetime = request.POST.getlist('time')
    name = request.POST['name']
    if len(name)>=5:
        newname=name[0:5]
    else:
        newname=name

    #获取值
    year = request.POST['year']
    month = request.POST['month']
    date = []
    haoping = []
    zhongping = []
    chaping = []
    print(year);
    print(month);
    if choosetime[0] == 'yue':
        dict1 = jingqu.get_month()

        list1 = dict1[newname][0]
        list2 = dict1[newname][1]
    elif choosetime[0] == 'zhou':
        dict1 = jingqu.get_week()
        list1 = dict1[newname][0]
        list2 = dict1[newname][1]
    elif choosetime[0] == 'tian':
        dict1 = jingqu.get_day()
        list1 = dict1[newname][0][-15:]  # 只取最近15天的数据
        list2 = dict1[newname][1][-15:]
    elif choosetime[0] == 'nian':
        dict1 = jingqu.get_year()
        list1 = dict1[newname][0]
        list2 = dict1[newname][1]
    dict2, dict3 = jingqu.get_message()
    list3 = dict2[newname]
    list4 = dict3[newname];
    print(111);
    print(dict1);
    print(222);
    print(dict2);
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
    return render(request, 'singlejq.html', {
        #'name': json.dumps(name),
        'list1': json.dumps(list1),
        'list2': list2,
        'message': message,
        'list3':date,
        'list4':chaping,
        'list5':zhongping,
        'list6':haoping,
        })