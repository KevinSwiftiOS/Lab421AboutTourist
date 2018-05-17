from ..initViews import *;
from django.shortcuts import render;
import json
def singlejq(request):
  # if request.is_ajax():
  #   #景区名是否合法
  #
  #   param =  json.loads((request.POST.get('param')));
  #
  #   choosetime = param["time"];
  #   name = param["name"];
  #   if len(name)>=5:
  #       newname=name[0:5]
  #   else:
  #       newname=name
  #
  #   # #获取值
  #   # year  = param["year"];
  #   # month = param["month"];
  # #开始于结束年月份
  #   startYear = int(param["startYear"]);
  #   startMonth = int(param["startMonth"]);
  #   endYear = int(param["endYear"]);
  #   endMonth = int(param["endMonth"]);
  #
  #
  #   message = [];
  #   list1 = [];
  #   list2 = [];
  #
  #   finData = [];
  #
  #   haoping = []
  #   zhongping = []
  #   chaping = []
  #   success = 0;
  #   xAxis = [];
  #   yAxis = [];
  #   date = [];
  #
  #   jingqu_name = jingqu.get_all_name();
  #
  #   for i in range(0,len(jingqu_name)):
  #    print (jingqu_name[i]);
  #    if newname == jingqu_name[i]:
  #
  #           success = 1;
  #
  #   if(success):
  #
  #     try:
  #         if choosetime == 'month':
  #             yearMonth = jingqu.get_year_month();
  #             print (yearMonth);
  #             # 遍历yearMonth 当年份和月份相同后 进行输出
  #             allMonth = yearMonth[newname];
  #
  #            #进行取值
  #             for year in allMonth:
  #
  #                 if year >= startYear and year <= endYear:
  #                     for month in allMonth[year]:
  #                         if month >= startMonth and year == startYear:
  #
  #                                  xAxis.append(str(year) + "." + str(month));
  #                                  yAxis.append(allMonth[year][month]);
  #
  #
  #                         elif month <= endMonth and year == endYear:
  #                             xAxis.append(str(year) + "." + str(month));
  #                             yAxis.append(allMonth[year][month]);
  #
  #                         elif year >= startYear & year <= endYear & month >= startMonth & month <= endMonth:
  #
  #                             xAxis.append(str(year) + "." + str(month));
  #                             yAxis.append(allMonth[year][month]);
  #
  #
  #         elif choosetime == 'year':
  #             yearMonth = jingqu.get_year_month();
  #
  #             print (yearMonth);
  #             # 遍历yearMonth 当年份和月份相同后 进行输出
  #             allMonth = yearMonth[newname];
  #
  #             # 进行取值
  #             for year in allMonth:
  #
  #                 if year >= startYear and year <= endYear:
  #                     monthCnt = 0;
  #                     for month in allMonth[year]:
  #                         monthCnt += allMonth[year][month];
  #
  #                     xAxis.append(str(year));
  #                     yAxis.append(monthCnt);
  #         elif choosetime == 'season':
  #             yearMonth = jingqu.get_year_month();
  #
  #             # 遍历yearMonth 当年份和月份相同后 进行输出
  #             allMonth = yearMonth[newname];
  #
  #             # 进行取值
  #             for year in allMonth:
  #
  #                 if year >= startYear and year <= endYear:
  #                     seasons = [0,0,0,0];
  #                     for month in allMonth[year]:
  #                         if month >= startMonth and year == startYear:
  #                             seasons[int(int(month) / 4)] +=  int(allMonth[year][month]);
  #
  #
  #                         elif month <= endMonth and year == endYear:
  #                             seasons[int(int(month) / 4)] += int(allMonth[year][month]);
  #
  #                         elif year >= startYear & year <= endYear & month >= startMonth & month <= endMonth:
  #                             seasons[int(int(month) / 4)] += int(allMonth[year][month]);
  #                      #并入xAxis和yAxis中
  #                     for i in  range(len(seasons)):
  #
  #                       if(seasons[i] != 0):
  #                           xAxis.append(str(year) + "年" + str(i + 1) + "季度");
  #                           yAxis.append(seasons[i]);
  #
  #         #
  #         # elif choosetime == 'zhou':
  #         #     dict1 = jingqu.get_week()
  #         #     list1 = dict1[newname][0]
  #         #     list2 = dict1[newname][1]
  #         # elif choosetime == 'tian':
  #         #     dict1 = jingqu.get_day()
  #         #     list1 = dict1[newname][0][-15:]  # 只取最近15天的数据
  #         #     list2 = dict1[newname][1][-15:]
  #         # elif choosetime == 'nian':
  #         #     dict1 = jingqu.get_year()
  #         #     list1 = dict1[newname][0]
  #         #     list2 = dict1[newname][1]
  #         dict2, dict3 = jingqu.get_message()
  #         list3 = dict2[newname]
  #         list4 = dict3[newname];
  #
  #         message = dict(zip(list4, list3))  # 将对应的打包成元祖
  #         dict4 = jingqu.get_score_message()
  #         list5 = sorted(dict4[newname].items(), key=lambda d: d[0])
  #
  #         for i, j in enumerate(list5):  # 进行遍历对象
  #             if int(j[0][0:4]) == startYear and int(j[0][5:7]) >= startMonth:
  #                 date.append(j[0])
  #                 j[1].setdefault('差评', 0)
  #                 j[1].setdefault('中评', 0)
  #                 j[1].setdefault('好评', 0)
  #                 haoping.append(j[1]['好评'])
  #                 zhongping.append(j[1]['中评'])
  #                 chaping.append(j[1]['差评'])
  #             elif int(j[0][0:4]) == endYear and int(j[0][5:7]) <= endMonth:
  #                 date.append(j[0])
  #                 j[1].setdefault('差评', 0)
  #                 j[1].setdefault('中评', 0)
  #                 j[1].setdefault('好评', 0)
  #                 haoping.append(j[1]['好评'])
  #                 zhongping.append(j[1]['中评'])
  #                 chaping.append(j[1]['差评'])
  #             elif int(j[0][0:4]) >= startYear and int(j[0][0:4]) <= endYear  and int(j[0][5:7]) <= endMonth and int(j[0][5:7]) >= startMonth:
  #                 date.append(j[0])
  #                 j[1].setdefault('差评', 0)
  #                 j[1].setdefault('中评', 0)
  #                 j[1].setdefault('好评', 0)
  #                 haoping.append(j[1]['好评'])
  #                 zhongping.append(j[1]['中评'])
  #                 chaping.append(j[1]['差评'])
  #
  #         param = {
  #              "code":0,
  #             "xAxis": xAxis,
  #             "yAxis": yAxis,
  #             "date": date,
  #             "chaping": chaping,
  #             "zhongping": zhongping,
  #             "haoping": haoping,
  #              "message": message,
  #         };
  #           # repr 将数字 列表转化为字符串 eval将字符串类型转化为字典
  #     except KeyError:
  #
  #      param = {
  #            "code": 1,
  #            "message":"未有该月的评论信息",
  #
  #
  #      };
  #   else:
  #    param = {
  #            "code": 2,
  #            "message":"请查看景区名字是否合法"
  #   };
  #   print (param);
  #   finalParam = eval(repr(param));
  #   return  JsonResponse(finalParam);
  # else:
  #   return render(request, 'singlejq.html');
    if request.is_ajax():
        print (111);

        dict = {}
        # 获取数据
        jqs = eval((request.POST.getlist('jqs'))[0]);

        platforms = eval((request.POST.getlist("platforms"))[0]);
        startYear = request.POST.get('startYear')
        startDate = request.POST.get('startDate')
        endYear = request.POST.get('endYear')
        endDate = request.POST.get('endDate')
        time = request.POST.get('time')
        print (jqs);
        print (platforms);
        # name = eval(name[0])
        # month = eval(month[0])
        data = {
            "jqs": [],
            "dates": [],
        };
        res = {

        }
        try:
            for i, jq in enumerate(jqs):
                jqs = {
                    "jq": jq,
                    "platforms": []
                };
                for j, platform in enumerate(platforms):
                    data['dates'], commentValue,gradeValue = getCommentsSingleJq(jq, platform, startYear, endYear, startDate, endDate, time);

                    value = {
                        "name": platform,
                        "commentValue": commentValue,
                        "gradeValue":gradeValue
                    }
                    jqs["platforms"].append(value);
                data["jqs"].append(jqs);

            res["data"] = data;
            res["code"] = 0;

            return JsonResponse(eval(repr(res)));


        except KeyError:

            res["code"] = 1;
            res["message"] = "映射中没有这个键";

        except TypeError:

            res["code"] = 2;
            res["message"] = "对类型无效的操作";


        return render(request, 'singlejq.html')

    else:

      return render(request, 'singlejq.html')