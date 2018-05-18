# from ..initViews import *;
# from django.shortcuts import render;
# import json
#
#
# def kindjq(request):
#     #判断景区名字的合法性
#
#  if request.is_ajax():
#      dict = {}
#      haoping = []
#      zhongping = []
#      chaping = []
#      success = 0;
#      pingtai = request.POST.getlist('pingtai')
#      year = request.POST.get('year')
#      month = request.POST.getlist('month')
#      name = request.POST.get("name");
#      jingqu_name = jingqu.get_all_name();
#      # for i in range(0, len(jingqu_name)):
#      #         if name == jingqu_name[i]:
#      #             success = 1;
#      #             break;
#
#      shops =  shops_data['data_region'];
#      shops_name_list = list(shops.values);
#      for i in range(len(shops_name_list)):
#           if name == shops_name_list[i]:
#              success = 1;
#              break;
#
#      if (success):
#          try:
#
#
#              jingqu_comments = comments_data[
#                  (comments_data['data_source'] == '景点') & (comments_data['data_region'] == name)]
#              jingqu_shops = shops_data[(shops_data['data_source'] == '景点') & (shops_data['data_region'] == name)]
#              kingJq = Ways(jingqu_comments, jingqu_shops)
#
#              monthIndexs, monthValues = kingJq.get_all_month()
#              yearIndexs, yearValues = kingJq.get_all_year()
#              weekIndexs, weekValues = kingJq.get_all_week()
#              dayIndexs, dayValues = kingJq.get_all_day()
#              dayIndexs = dayIndexs[-15:]
#              dayValues = dayValues[-15:]
#              dict["monthIndexs"] = monthIndexs;
#              dict["monthValues"] = monthValues;
#              dict["yearIndexs"] = yearIndexs;
#              dict["yearValues"] = yearValues;
#              dict["weekIndexs"] = weekIndexs;
#              dict["weekValues"] = weekValues;
#              dict["dayIndexs"] = dayIndexs;
#              dict["dayValues"] = dayValues;
#
#
#
#              if len(eval(pingtai[0])) == 1:
#                  # 平台上的对景区的评价
#                  # 进行删选
#                  pt_jingqu = get_pingtai(eval(pingtai[0]), jingqu_shops, jingqu_comments, 0)
#                  list1, list2 = pt_jingqu.get_all_month()
#                  dict['month'] = list1
#                  dict['month_number'] = list2
#                  dict = eval(repr(dict))
#              else:
#                  number = len(eval(pingtai[0]))
#                  dict['month_number'] = []
#                  for i in range(number):
#                      # 第i个景区进行删选
#                      pt_jingqu = get_pingtai(eval(pingtai[0]), jingqu_shops, jingqu_comments, i)
#                      list1, list2 = pt_jingqu.get_all_month()
#                      dict['month'] = list1
#                      dict['month_number'].append(list2)
#              score = jingqu.get_score_month()
#              for i in range(len(eval(month[0]))):
#                  month_choose = score[int(year)][int(eval(month[0])[i])]
#                  month_choose = get_pingjia(month_choose)
#                  haoping.append(month_choose['好评'])
#                  zhongping.append(month_choose['中评'])
#                  chaping.append(month_choose['差评'])
#              dict['haoping'] = haoping
#              dict['zhongping'] = zhongping
#              dict['chaping'] = chaping
#              dict["code"] = 0;
#              score2 = jingqu.get_score_day()
#              year_month = jingqu.get_all_year_month()
#
#          except KeyError:
#              dict["code"] = 1;
#              dict["message"] = "未有该月评论信息"
#
#      else:
#         dict["code"] = 2;
#         dict["message"] = "查看名字是否合法"
#      print(dict)
#      dict = eval(repr(dict))
#      return JsonResponse(dict)
#
#  else:
#      return render(request, 'kindjq.html');
#
from ..initViews import *;
from django.shortcuts import render;
import json


def ComparedAnalysis(request):

    if request.is_ajax():


        # 获取数据
        years = eval((request.POST.getlist('years'))[0]);

        platforms = eval((request.POST.getlist("platforms"))[0]);
        startDate = request.POST.get('startDate')
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

                resplatforms = {
                    "platform": platform,
                    "years": []
                };
                for j, year in enumerate(years):
                    comments['dates'], commentsValue,gradeValue = getCommentsComparedAnalysis(year, platform, startDate, endDate, time);

                    value = {
                        "year": year,
                        "commentValue": commentsValue,
                         "gradeValue":gradeValue
                    }
                    resplatforms["years"].append(value);
                comments["platforms"].append(resplatforms);

            res["data"] = comments;
            res["code"] = 0;

            return JsonResponse(eval(repr(res)));



        except KeyError:

            res["code"] = 1;
            res["message"] = "映射中没有这个键";

        except TypeError:

            res["code"] = 2;
            res["message"] = "对类型无效的操作";

        return render(request, 'ComparedAnalysis.html')

    else:

      return render(request, 'ComparedAnalysis.html')








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

