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

    # #获取值
    # year  = param["year"];
    # month = param["month"];
  #开始于结束年月份
    startYear = int(param["startYear"]);
    startMonth = int(param["startMonth"]);
    endYear = int(param["endYear"]);
    endMonth = int(param["endMonth"]);

    print (choosetime);
    message = [];
    list1 = [];
    list2 = [];

    finData = [];

    haoping = []
    zhongping = []
    chaping = []
    success = 0;
    xAxis = [];
    yAxis = [];
    date = [];
    print (choosetime);
    jingqu_name = jingqu.get_all_name();
    for i in range(0,len(jingqu_name)):
     if newname == jingqu_name[i]:
            success = 1;
            break;
    if(success):

      try:
          if choosetime == 'month':
              yearMonth = jingqu.get_year_month();
              print (yearMonth);

              # 遍历yearMonth 当年份和月份相同后 进行输出
              allMonth = yearMonth[newname];
              print (111);
              print (allMonth);
             #进行取值
              for year in allMonth:

                  if year >= startYear and year <= endYear:
                      for month in allMonth[year]:
                          if month >= startMonth and year == startYear:

                                   xAxis.append(str(year) + "." + str(month));
                                   yAxis.append(allMonth[year][month]);


                          elif month <= endMonth and year == endYear:
                              xAxis.append(str(year) + "." + str(month));
                              yAxis.append(allMonth[year][month]);

                          elif year >= startYear & year <= endYear & month >= startMonth & month <= endMonth:
                              print (34456);
                              xAxis.append(str(year) + "." + str(month));
                              yAxis.append(allMonth[year][month]);


          elif choosetime == 'year':
              yearMonth = jingqu.get_year_month();
              print (yearMonth);

              # 遍历yearMonth 当年份和月份相同后 进行输出
              allMonth = yearMonth[newname];
              print (111);
              print (allMonth);
              # 进行取值
              for year in allMonth:
                  print (year);
                  if year >= startYear and year <= endYear:
                      monthCnt = 0;
                      for month in allMonth[year]:
                          monthCnt += allMonth[year][month];

                      xAxis.append(str(year));
                      yAxis.append(monthCnt);



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

          message = dict(zip(list4, list3))  # 将对应的打包成元祖
          dict4 = jingqu.get_score_message()
          list5 = sorted(dict4[newname].items(), key=lambda d: d[0])
          for i, j in enumerate(list5):  # 进行遍历对象
              if int(j[0][0:4]) == startYear and int(j[0][5:7]) >= startMonth:
                  date.append(j[0])
                  j[1].setdefault('差评', 0)
                  j[1].setdefault('中评', 0)
                  j[1].setdefault('好评', 0)
                  haoping.append(j[1]['好评'])
                  zhongping.append(j[1]['中评'])
                  chaping.append(j[1]['差评'])
              elif int(j[0][0:4]) == endYear and int(j[0][5:7]) <= endMonth:
                  date.append(j[0])
                  j[1].setdefault('差评', 0)
                  j[1].setdefault('中评', 0)
                  j[1].setdefault('好评', 0)
                  haoping.append(j[1]['好评'])
                  zhongping.append(j[1]['中评'])
                  chaping.append(j[1]['差评'])
              elif int(j[0][0:4]) >= startYear and int(j[0][0:4]) <= endYear  and int(j[0][5:7]) <= endMonth and int(j[0][5:7]) >= startMonth:
                  date.append(j[0])
                  j[1].setdefault('差评', 0)
                  j[1].setdefault('中评', 0)
                  j[1].setdefault('好评', 0)
                  haoping.append(j[1]['好评'])
                  zhongping.append(j[1]['中评'])
                  chaping.append(j[1]['差评'])

          param = {
              "success": success,
              "xAxis": xAxis,
              "yAxis": yAxis,
              "date": date,
              "chaping": chaping,
              "zhongping": zhongping,
              "haoping": haoping,
               "message": message,
          };
            # repr 将数字 列表转化为字符串 eval将字符串类型转化为字典
      except KeyError:

       param = {
            "success": success,
             "xAxis":xAxis,
              "yAxis": yAxis,

              "chaping": chaping,
              "zhongping": zhongping,
              "haoping": haoping,
               "message": message,

       };
    else:
     param = {
            "success": success,
             "error":"请查看景区名字是否合法"
    };
    finalParam = eval(repr(param));
    return  JsonResponse(finalParam);
  else:
    return render(request, 'singlejq.html');