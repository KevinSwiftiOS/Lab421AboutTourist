from ..initViews import *;
from django.shortcuts import render;
import json


def alljq(request):
    if request.is_ajax():
        dict = {}
        name = request.POST.getlist('jq')
        year = request.POST.get('year')
        month = request.POST.getlist('month')
        name = eval(name[0])
        month = eval(month[0])
        for i,j in enumerate(name):
            haoping = []
            zhongping = []
            chaping = []
            dict[j] = {}
            jingqu_comments = comments_data[
                (comments_data['data_source'] == '景点') & (comments_data['data_region'] == j)]
            jingqu_shops = shops_data[(shops_data['data_source'] == '景点') & (shops_data['data_region'] == j)]
            jingqu = Ways(jingqu_comments, jingqu_shops)
            list1,list2 = jingqu.get_all_month()
            dict[j]['month'] = list1
            dict[j]['month_number'] = list2
            score = jingqu.get_score_month()
      #      print(score)
            for k in range(len(month)):
                month_choose = score[int(year)][int(month[k])]
                month_choose = get_pingjia(month_choose)
                haoping.append(month_choose['好评'])
                zhongping.append(month_choose['中评'])
                chaping.append(month_choose['差评'])
            dict[j]['haoping'] = haoping
            dict[j]['zhongping'] = zhongping
            dict[j]['chaping'] = chaping
        dict = eval(repr(dict))
        return JsonResponse(dict)
    else:
        return render(request,'alljq.html')
