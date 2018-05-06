from ..initViews import *;
from django.shortcuts import render;
import json


def kindjq(request):
    global name
    if request.is_ajax():
     #   print(name)
        jingqu_comments = comments_data[
            (comments_data['data_source'] == '景点') & (comments_data['data_region'] == name)]
        jingqu_shops = shops_data[(shops_data['data_source'] == '景点') & (shops_data['data_region'] == name)]
      #  print(len(jingqu_shops))
        jingqu = Ways(jingqu_comments, jingqu_shops)
        haoping = []
        zhongping = []
        chaping = []
        pingtai = request.POST.getlist('pingtai')
        year = request.POST.get('year')
        month = request.POST.getlist('month')
        dict = {}
        if len(eval(pingtai[0]))==1:
            pt_jingqu = get_pingtai(eval(pingtai[0]),jingqu_shops,jingqu_comments,0)
            list1,list2 = pt_jingqu.get_all_month()
            dict['month'] = list1
            dict['month_number'] = list2
            dict = eval(repr(dict))
        else:
            number = len(eval(pingtai[0]))
            dict['month_number'] = []
            for i in range(number):
                pt_jingqu = get_pingtai(eval(pingtai[0]),jingqu_shops,jingqu_comments,i)
                list1,list2 = pt_jingqu.get_all_month()
                dict['month'] = list1
                dict['month_number'].append(list2)
        score = jingqu.get_score_month()
        for i in range(len(eval(month[0]))):
            month_choose = score[int(year)][int(eval(month[0])[i])]
            month_choose = get_pingjia(month_choose)
            haoping.append(month_choose['好评'])
            zhongping.append(month_choose['中评'])
            chaping.append(month_choose['差评'])
        dict['haoping'] = haoping
        dict['zhongping'] = zhongping
        dict['chaping'] = chaping
        score2 = jingqu.get_score_day()
        year_month = jingqu.get_all_year_month()
       # print(dict)
        dict = eval(repr(dict))
        return JsonResponse(dict)
    else:
        name = request.POST['name']
        jingqu_comments = comments_data[
            (comments_data['data_source'] == '景点') & (comments_data['data_region'] == name)]
        jingqu_shops = shops_data[(shops_data['data_source'] == '景点') & (shops_data['data_region'] == name)]
        jingqu = Ways(jingqu_comments, jingqu_shops)
        list1, list2 = jingqu.get_all_month()
        list3, list4 = jingqu.get_all_year()
        list5, list6 = jingqu.get_all_week()
        list7, list8 = jingqu.get_all_day()
        list7 = list7[-15:]
        list8 = list8[-15:]
        return render(request,'kindjq.html',{
            'name': name,
            'list1': json.dumps(list1),
            'list2': list2,
            'list3': json.dumps(list3),
            'list4': list4,
            'list5': json.dumps(list5),
            'list6': list6,
            'list7': json.dumps(list7),
            'list8': list8,
        })