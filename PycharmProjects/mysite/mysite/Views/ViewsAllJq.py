from ..initViews import *;
from django.shortcuts import render;
import json


def alljq(request):
    if request.is_ajax():

        dict = {}
        # 获取数据
        jqs = eval((request.POST.getlist('jqs'))[0]);

        platforms = eval((request.POST.getlist("platforms"))[0]);
        startYear = request.POST.get('startYear')
        startDate = request.POST.get('startDate')
        endYear = request.POST.get('endYear')
        endDate = request.POST.get('endDate')
        time = request.POST.get('time')

        # name = eval(name[0])
        # month = eval(month[0])
        comments = {
            "platforms": [],
            "dates": [],
        };
        res = {

        }
        try:
            for i, platform in enumerate(platforms):
                platforms = {
                    "platform": platform,
                    "jqs": []
                };
                for j, jq in enumerate(jqs):
                    comments['dates'], commentsValue,gradeValue = getCommentsAllJq(jq, platform, startYear, endYear, startDate, endDate, time);

                    jq = {
                        "name": jq,
                        "commentValue": commentsValue,
                         "gradeValue":gradeValue
                    }
                    platforms["jqs"].append(jq);
                    comments["platforms"].append(platforms);

            res["data"] = comments;
            res["code"] = 0;

            return JsonResponse(eval(repr(res)));



        except KeyError:

            res["code"] = 1;
            res["message"] = "映射中没有这个键";

        except TypeError:

            res["code"] = 2;
            res["message"] = "对类型无效的操作";

        return render(request, 'alljq.html')

    else:

      return render(request, 'alljq.html')








    #       for i,j in enumerate(name):
    #         haoping = []
    #         zhongping = []
    #         chaping = []
    #         months = [];
    #         dict[j] = {}
    #         jingqu_comments = comments_data[
    #             (comments_data['data_source'] == '景点') & (comments_data['data_region'] == j)]
    #         jingqu_shops = shops_data[(shops_data['data_source'] == '景点') & (shops_data['data_region'] == j)]
    #         jingqu = Ways(jingqu_comments, jingqu_shops)
    #         list1,list2 = jingqu.get_all_month()
    #         dict[j]['month'] = list1
    #         dict[j]['month_number'] = list2
    #         score = jingqu.get_score_month()
    #         print(score)
    #         for k in range(len(month)):
    #             month_choose = score[int(year)][int(month[k])]
    #             month_choose = get_pingjia(month_choose)
    #             haoping.append(month_choose['好评'])
    #             zhongping.append(month_choose['中评'])
    #             chaping.append(month_choose['差评'])
    #             months.append(int(month[k]));
    #         dict[j]['haoping'] = haoping
    #         dict[j]['zhongping'] = zhongping
    #         dict[j]['chaping'] = chaping
    #         dict[j]['gradeMonths'] = months;
    #       dict["code"] = 0;
    #       dict = eval(repr(dict))
    #       print (333);
    #       print (dict);
    #     except KeyError:
    #       print (555);
    #       dict["code"] = 1;
    #       dict["message"] = "选择月份未有评论信息";
    #       dict = eval(repr(dict));
    #       print (dict);

