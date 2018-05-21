from ..initViews import *;
from django.shortcuts import render;
import json
def RecentState(request):

    if request.is_ajax():
        res = {};
        comments = {
            "times": [],
            "platforms":[]
        };
        try:

            jq = request.POST.get("jq");
            #八大平台上都进行获取
            platforms = ['携程', '艺龙', '去哪儿', '驴妈妈', '马蜂窝', '途牛', '飞猪', '大众点评'];
            comments["platforms"] = platforms;
            #时间间隔分为年月季度周
            times = ["year","season","month","week"];
            dic = {
                'year':"过去一年",
                "season":"过去一季度",
                "month":"过去一月",
                "week":"过去一周"
            }
            #进行遍历获取值
            for i,time in enumerate(times):
                restimes = {
                    "time": dic[time],
                    "platforms": []
                };
                for j,platform in enumerate(platforms):

                    commentValue,gradeValue = getCommentsRecentState(time,platform,jq);

                    value = {
                        "name":platform,
                        "commentValue": commentValue,
                        "gradeValue": gradeValue
                    }
                    restimes["platforms"].append(value)
                comments["times"].append(restimes);
            res["data"] = comments;
            res["code"] = 0;

            return JsonResponse(eval(repr(res)));
        except KeyError:

            res["code"] = 1;
            res["message"] = "映射中没有这个键";
            return render(request, 'RecentState.html')
        except TypeError:

            res["code"] = 2;
            res["message"] = "对类型无效的操作";

            return render(request, 'RecentState.html')


    else:
      print(2);
      return render(request, 'RecentState.html')