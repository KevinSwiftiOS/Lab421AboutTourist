
from __future__ import unicode_literals #版本的兼容性
import pandas as pd

import re
import json
from django.shortcuts import render
import pymongo
from pandas import Series,DataFrame
import time
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.http import JsonResponse
import datetime
import math
import  csv


client = pymongo.MongoClient('localhost',27517)

database = client['dspider2']
#读入数据
# shops_data = DataFrame(pd.read_csv('/home/ckq/文档/github/Lab421AboutTourist/shops_data_54.csv',sep = ' '));
# comments_data = DataFrame(pd.read_csv('/home/ckq/文档/github/Lab421AboutTourist/comments_data_54.csv',sep = ' '));
#dframe1 = pd.read_excel("/Users/hcnucai/Desktop/Lab421/comment_data\(UTF-8\)5.4.xlsx",sheetname="Sheet1");
comments_tb = database.comments;
shops_tb = database.shops;

shops_data = DataFrame(list(shops_tb.find()))
comments_data = DataFrame(list(comments_tb.find()))

def change1(name):
    if name is np.nan:
        return name
    #字符串操作 倒数第二个字符
    if name[-2:]=='景区':
        return name[0:-2]
    elif name[-1]=='区' and name[-2]!='景':
        return name[0:-1]
    else:
        return name
def rename(name):
    if name is np.nan:
        return name
    if len(name)>=5:
        return name[0:5]

    else:
        return name
def convert_time(words):
    if pd.isnull(words):
        return '2000-01-01'
    elif len(words) <= 5:
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))
    elif words[0]=='发':
        return words[3:]
    else:
        return words
def change2(words):
    if pd.isnull(words) or words is np.nan:
        return words
    elif int(words) == 1 or int(words) == 2:
        words = "差评"
    elif int(words) == 3:
        words = "中评"
    else:
        words = "好评"
    return words
def week(words):
    #用秒数来表示时间的浮点数
    a = time.mktime(time.strptime(words, '%Y-%m-%d')) #strptime据指定的格式把一个时间字符串解析为时间元组 mktime返回用秒数来表示时间的浮点数。
    timestruct = time.localtime(a)
    return int(time.strftime('%W', timestruct)) #返回一年中的星期数
#季度
def season(month):
      if (month % 3 == 0):
          return  int(month / 3);
      else:
       return  int(math.floor(month / 3) + 1);
def changeCommentGrade(grade):

    if pd.isnull(grade) or grade is np.nan:

        return 0;
    else:
        return grade;
def comments_convert(data):
    #字符串进行合并
    data['shop_name'] = data['shop_name'].apply(change1)
    name = data['shop_name'].value_counts().index

    data['newname'] = data['shop_name'] #去掉rename
    data['comment_time'] = data['comment_time'].apply(convert_time)
    data['year'] = data['comment_time'].apply(lambda x: int(x[0:4]) if x is not np.nan else x)
    data['month'] = data['comment_time'].apply(lambda x: int(x[5:7]) if x is not np.nan else x)
    data['day'] = data['comment_time'].apply(lambda x: x[0:10] if x is not np.nan else x)
    data['comment_score'] = data['comment_score'].apply(changeCommentGrade)
    data['week'] = data['day'].apply(week)
    data['weekday'] = data['day'].apply(lambda x:pd.to_datetime(x).weekday())
    data['pingjia'] = data['comment_score'].apply(change2)

   # data['yearMonth'] = data.apply(lambda x:'%s.%s' %(data['year'],data['month']),axis = 1);
    data['yearMonth'] = data['year'].astype(str) + '.' + data['month'].astype(str)
    data['season'] = data['month'].apply(season);
    data['yearSeason'] = data['year'].astype(str) + '.' + data['season'].astype(str)
    data['yearWeek'] = data['year'].astype(str) + '.' + data['week'].astype(str)

    return data
def shops_convert(data):
    data['shop_name'] = data['shop_name'].apply(change1)
    data['newname'] = data['shop_name']#去掉rename
    name = data['newname'].value_counts().index #记录频数
    all = []
    for i in range(len(name)):
        a = data[data['newname']==name[i]]
        a = a.fillna(method='bfill') #用指定值或插值方法（如ffill和bfill）填充缺失数据
        all.append(a.iloc[0]) #索引第一行
    data = DataFrame(all)
    return data
#函数名中含有all的表示的是总体的情况,没有的是单个景区的情况
class Ways():
    def __init__(self,data1,data2):
        self.comments = data1
        self.shops = data2
        self.jingqu_name = data2['newname'].value_counts().index
    def get_all_year(self):#每年评论数量的变化 单个景区的
        a = self.comments['year'].value_counts().sort_index()
        indexlist = list(a.index)
        valuelist = list(a.values)
        return indexlist, valuelist

    def get_all_month(self):#每个月评论数量的变化
        a = self.comments['month'].value_counts().sort_index()
        indexlist = list(a.index)
        valuelist = list(a.values)
        return indexlist, valuelist

    def get_all_day(self):#每天评论数量的变化
        a = self.comments['day'].value_counts().sort_index()
        indexlist = list(a.index)
        valuelist = list(a.values)
        return indexlist, valuelist
    def get_all_week(self):#每周评论数量的变化
        end = self.comments['day'].max()
        num = self.comments[self.comments['day'] == end].iloc[0].weekday
        x = datetime.datetime.strptime(end,"%Y-%m-%d")
        if num==0:
            newend = x
        else:
            newend = x+datetime.timedelta(days=-int(num))
        y = newend+datetime.timedelta(weeks=-3)
        start = y.strftime('%Y-%m-%d')
        shuju = comments_data[(comments_data['day'] >= start) & (comments_data['day'] <= end)]
        a = shuju['week'].value_counts().sort_index()
        indexlist = list(a.index)
        valuelist = list(a.values)
        return indexlist, valuelist
    def get_all_year_month(self):#评论数量每年每个月的变化
        year_month = {}
        a = self.comments.groupby(['year', 'month']).size().reset_index().rename(columns={0: 'count'})
        for i in range(len(a)):
            if a.iloc[i, 0] not in year_month:
                year_month[a.iloc[i, 0]] = {}
                year_month[a.iloc[i, 0]][a.iloc[i, 1]] = a.iloc[i, 2]
            elif a.iloc[i, 0] in year_month and a.iloc[i, 1] not in year_month[a.iloc[i, 0]]:
                year_month[a.iloc[i, 0]][a.iloc[i, 1]] = a.iloc[i, 2]
        return year_month

    def get_all_ymd(self):#评论数量每年每月每天的变化
        ymd = {}
        b = self.comments.groupby(['year', 'month', 'day']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i, 0] not in ymd:
                ymd[b.iloc[i, 0]] = {}
                ymd[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                ymd[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in ymd and b.iloc[i, 1] not in ymd[b.iloc[i, 0]]:
                ymd[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                ymd[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in ymd and b.iloc[i, 1] in ymd[b.iloc[i, 0]] and b.iloc[i, 2] not in \
                    ymd[b.iloc[i, 0]][b.iloc[i, 1]]:
                ymd[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return ymd

    def get_score_month(self):#好中差评随月份的变化
        score_month = {}
        b = self.comments.groupby(['year', 'month', 'pingjia']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i, 0] not in score_month:
                score_month[b.iloc[i, 0]] = {}
                score_month[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in score_month and b.iloc[i, 1] not in score_month[b.iloc[i, 0]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in score_month and b.iloc[i, 1] in score_month[b.iloc[i, 0]] and b.iloc[i, 2] not in \
                    score_month[b.iloc[i, 0]][b.iloc[i, 1]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return score_month

    def get_score_day(self):#好中差评随天的变化
        score_day = {}
        b = self.comments.groupby(['day', 'pingjia']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i, 0] not in score_day:
                score_day[b.iloc[i, 0]] = {}
                score_day[b.iloc[i, 0]][b.iloc[i, 1]] = b.iloc[i, 2]
            elif b.iloc[i, 0] in score_day and b.iloc[i, 1] not in score_day[b.iloc[i, 0]]:
                score_day[b.iloc[i, 0]][b.iloc[i, 1]] = b.iloc[i, 2]
        return score_day
    def get_year(self):#评论数量随年的变化
        all = {}
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]] = []
            a = self.comments[self.comments['newname'] == self.jingqu_name[i]]
            b = a['year'].value_counts().sort_index()
            all[self.jingqu_name[i]].append(list(b.index))
            all[self.jingqu_name[i]].append(list(b.values))
        return all

    def get_month(self):#评论数量随月的变化

        all = {}
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]] = []
            a = self.comments[self.comments['newname'] == self.jingqu_name[i]]

            b = a['month'].value_counts().sort_index()


            all[self.jingqu_name[i]].append(list(b.index))
            all[self.jingqu_name[i]].append(list(b.values))

        return all
     #获取一个月的
    def get_one_month(self):
        all = {};

    def get_day(self):#评论数量随天的变化
        all = {}
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]] = []
            a = self.comments[self.comments['newname'] == self.jingqu_name[i]]
            b = a['day'].value_counts().sort_index()
            all[self.jingqu_name[i]].append(list(b.index))
            all[self.jingqu_name[i]].append(list(b.values))
        return all
    def get_year_month(self):#评论数量每年每月的变化
        all = {}
        for i in range(len(self.jingqu_name)):
            x = self.comments[self.comments['newname'] == self.jingqu_name[i]]
            year_month = {}
            a = x.groupby(['year', 'month']).size().reset_index().rename(columns={0: 'count'})
            for i in range(len(a)):
                if a.iloc[i, 0] not in year_month:
                    year_month[a.iloc[i, 0]] = {}
                    year_month[a.iloc[i, 0]][a.iloc[i, 1]] = a.iloc[i, 2]
                elif a.iloc[i, 0] in year_month and a.iloc[i, 1] not in year_month[a.iloc[i, 0]]:
                    year_month[a.iloc[i, 0]][a.iloc[i, 1]] = a.iloc[i, 2]
            all[self.jingqu_name[i]] = year_month
        return all
    def get_week(self):#评论数量每周的变化
        all={}
        end = self.comments['day'].max()
        num = self.comments[self.comments['day'] == end].iloc[0].weekday
        x = datetime.datetime.strptime(end, "%Y-%m-%d")
        if num == 0:
            newend = x
        else:
            newend = x + datetime.timedelta(days=-int(num))
        y = newend + datetime.timedelta(weeks=-3)
        start = y.strftime('%Y-%m-%d')
        shuju = comments_data[(comments_data['day'] >= start) & (comments_data['day'] <= end)]
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]] = []
            a = shuju[shuju['newname'] == self.jingqu_name[i]]
            b = a['week'].value_counts().sort_index()
            all[self.jingqu_name[i]].append(list(b.index))
            all[self.jingqu_name[i]].append(list(b.values))
        return all

    def get_message(self):#获得单个景区的信息
        choose = ['_id','comment_url','crawl_time','shop_active','shop_detail_url','data_website','shop_active ','shop_url','shop_img','shop_id','newname',]
        all = {}
        allcolumns = {}
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]] = []
            allcolumns[self.jingqu_name[i]] = []
            a = self.shops[self.shops['newname'] == self.jingqu_name[i]]
            for j in range(len(a.columns)):
                if pd.isnull(a[a.columns[j]].iloc[0]) or a.columns[j] in choose or len(str(a[a.columns[j]].iloc[0]))==0:
                    continue
                else:
                    all[self.jingqu_name[i]].append(a[a.columns[j]].iloc[0])
                    allcolumns[self.jingqu_name[i]].append(a.columns[j])
        return all,allcolumns

    def get_score_message(self):#好中差评随天的变化
        score_message = {}
        b = self.comments.groupby(['newname', 'day', 'pingjia']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i, 0] not in score_message:
                score_message[b.iloc[i, 0]] = {}
                score_message[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_message[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in score_message and b.iloc[i, 1] not in score_message[b.iloc[i, 0]]:
                score_message[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_message[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in score_message and b.iloc[i, 1] in score_message[b.iloc[i, 0]] and b.iloc[i, 2] not in \
                    score_message[b.iloc[i, 0]][b.iloc[i, 1]]:
                score_message[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return score_message
    def get_all_name(self): #获取所有的景区名字
        return self.jingqu_name;



comments_data = comments_convert(comments_data)
shops_data = shops_convert(shops_data)
#专门指千岛湖的
jingqu_comments = comments_data[(comments_data['data_source']=='景点')&(comments_data['data_region']=='千岛湖')]
jingqu_shops = shops_data[(shops_data['data_source']=='景点')&(shops_data['data_region']=='千岛湖')]
jingqu = Ways(jingqu_comments,jingqu_shops)
comments_data;
shops_data;
jingqu_comments;
jingqu_shops;
jingqu;

def get_pingtai(pingtai,a,b,num):
    pt_shops = a[a['data_website']==pingtai[num]]
    pt_comments = b[b['data_website']==pingtai[num]]
    pt_jingqu = Ways(pt_comments,pt_shops)
    return pt_jingqu
def get_pingjia(a):
    a.setdefault('差评', 0)
    a.setdefault('中评', 0)
    a.setdefault('好评', 0)
    return a


#所有景区根据时间间隔 平台 景点 获取评论数
def getGradesAllJq(jq,platform,startYear,endYear,startDate,endDate,time):
    values = [];
    dates = [];
    jq_comment_data = comments_data[(comments_data['data_source'] == '景点') & (comments_data['data_region'] == jq)];
    ends = 0;
    yearDate = "";
    if(time == 'season'):
        ends = 5;
        yearDate = "yearSeason";
    elif time == 'month':
        ends = 13;
        yearDate = "yearMonth";
    elif time == 'week':
        ends = 53;
        yearDate = "yearWeek";
    if time == 'year':

        for year in range(int(startYear), int(endYear) + 1):
            jq_comment_year = jq_comment_data[
                (jq_comment_data['data_website'] == platform) & (jq_comment_data['year'] == int(year))];
            if(round(jq_comment_year['comment_score'].mean() is np.nan)):
              values.append(0);
            else:
              values.append(round(jq_comment_year['comment_score'].mean(), 1));
            dates.append(year);


#千岛湖环比分析根据时间间隔 平台 景点 获取评论数
def getCommentsCircularAnalysis(jq,platform,startYear,endYear,startDate,endDate,time):
    commentsValues = [];
    gradesValues = [];
    dates = [];

    ends = 0;
    yearDate = "";
    if(time == 'season'):
        ends = 5;
        yearDate = "yearSeason";
    elif time == 'month':
        ends = 13;
        yearDate = "yearMonth";
    elif time == 'week':
        ends = 53;
        yearDate = "yearWeek";

    jq_comment_data = comments_data[(comments_data['data_source'] == '景点') & (comments_data['data_region'] == jq)];

    if time == 'year':


        for year in range(int(startYear), int(endYear) + 1):
            jq_comments = jq_comment_data[
                (jq_comment_data['data_website'] == platform) & (jq_comment_data['year'] == int(year))];

            commentsValues.append(jq_comments.iloc[:, 0].size);
            if (round(jq_comments['comment_score'].mean() is np.nan)):
                gradesValues.append(0);
            else:
                gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
            dates.append(year);

    else:
        if (int(startYear) != int(endYear)):
            for year in range(int(startYear), int(endYear) + 1):
                if (int(year) == int(startYear)):
                    for date in range(int(startDate), ends):
                        yearDates = str(year) + '.' + str(date)

                        jq_comments = jq_comment_data[
                            (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];

                        commentsValues.append(jq_comments.iloc[:, 0].size);
                        if (round(jq_comments['comment_score'].mean() is np.nan)):
                            gradesValues.append(0);
                        else:
                            gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
                        dates.append(yearDates);
                elif (int(year) == int(endYear)):

                    for date in range(1, int(endDate) + 1):
                        yearDates = str(year) + '.' + str(date)
                        jq_comments = jq_comment_data[
                            (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];
                        commentsValues.append(jq_comments.iloc[:, 0].size);
                        if (round(jq_comments['comment_score'].mean() is np.nan)):
                            gradesValues.append(0);
                        else:
                            gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
                        dates.append(yearDates);
                else:

                    for date in range(1, ends):
                        yearDates = str(year) + '.' + str(date)
                        jq_comments = jq_comment_data[
                            (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];
                        commentsValues.append(jq_comments.iloc[:, 0].size);
                        if (round(jq_comments['comment_score'].mean() is np.nan)):
                            gradesValues.append(0);
                        else:
                            gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
                        dates.append(yearDates);

        else:
            for date in range(int(startDate), int(endDate) + 1):
                yearDates = str(startYear) + '.' + str(date)
                jq_comments = jq_comment_data[
                    (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];
                commentsValues.append(jq_comments.iloc[:, 0].size);
                if (round(jq_comments['comment_score'].mean() is np.nan)):
                    gradesValues.append(0);
                else:
                    gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
                dates.append(yearDates);




    return dates,commentsValues,gradesValues;
#千岛湖内部单个景区根据平台 开始 结束 时间间隔的变化
def getCommentsInnerScenic(jq,platform,startYear,endYear,startDate,endDate,time):
    commentsValues = [];
    gradesValues = [];
    dates = [];
    jq_comment_data = comments_data[(comments_data['data_source'] == '景点') & (comments_data['data_region'] == '千岛湖') & (
    comments_data['shop_name'] == jq)];

    ends = 0;
    yearDate = "";
    if (time == 'season'):
        ends = 5;
        yearDate = "yearSeason";
    elif time == 'month':
        ends = 13;
        yearDate = "yearMonth";
    elif time == 'week':
        ends = 53;
        yearDate = "yearWeek";

    if time == 'year':

        for year in range(int(startYear), int(endYear) + 1):
            jq_comments = jq_comment_data[
                (jq_comment_data['data_website'] == platform) & (jq_comment_data['year'] == int(year))];

            commentsValues.append(jq_comments.iloc[:, 0].size);
            if (round(jq_comments['comment_score'].mean() is np.nan)):
                gradesValues.append(0);
            else:
                gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
            dates.append(year);
    else:
        if (int(startYear) != int(endYear)):
            for year in range(int(startYear), int(endYear) + 1):
                if (int(year) == int(startYear)):
                    for date in range(int(startDate), ends):
                        yearDates = str(year) + '.' + str(date)

                        jq_comments = jq_comment_data[
                            (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];

                        commentsValues.append(jq_comments.iloc[:, 0].size);
                        if (round(jq_comments['comment_score'].mean() is np.nan)):
                            gradesValues.append(0);
                        else:
                            gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
                        dates.append(yearDates);
                elif (int(year) == int(endYear)):

                    for date in range(1, int(endDate) + 1):
                        yearDates = str(year) + '.' + str(date)
                        jq_comments = jq_comment_data[
                            (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];
                        commentsValues.append(jq_comments.iloc[:, 0].size);
                        if (round(jq_comments['comment_score'].mean() is np.nan)):
                            gradesValues.append(0);
                        else:
                            gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
                        dates.append(yearDates);
                else:

                    for date in range(1, ends):
                        yearDates = str(year) + '.' + str(date)
                        jq_comments = jq_comment_data[
                            (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];
                        commentsValues.append(jq_comments.iloc[:, 0].size);
                        if (round(jq_comments['comment_score'].mean() is np.nan)):
                            gradesValues.append(0);
                        else:
                            gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
                        dates.append(yearDates);

        else:
            for date in range(int(startDate), int(endDate) + 1):
                yearDates = str(startYear) + '.' + str(date)
                jq_comments = jq_comment_data[
                    (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];
                commentsValues.append(jq_comments.iloc[:, 0].size);
                if (round(jq_comments['comment_score'].mean() is np.nan)):
                    gradesValues.append(0);
                else:
                    gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
                dates.append(yearDates);
    return dates,commentsValues,gradesValues;


#千岛湖同比分析数据的获取
def getCommentsComparedAnalysis(year, platform, startDate, endDate, time):
    commentsValues = [];
    gradesValues = [];
    dates = [];
    yearDate = "";
    if (time == 'season'):

        yearDate = "yearSeason";
    elif time == 'month':

        yearDate = "yearMonth";
    elif time == 'week':

        yearDate = "yearWeek";

    jq_comment_data = comments_data[(comments_data['data_source'] == '景点') & (comments_data['data_region'] == '千岛湖')];

    if time == 'year':

            jq_comments = jq_comment_data[
                (jq_comment_data['data_website'] == platform) & (jq_comment_data['year'] == int(year))];

            commentsValues.append(jq_comments.iloc[:, 0].size);
            if (round(jq_comments['comment_score'].mean() is np.nan)):
                gradesValues.append(0);
            else:
                gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
            dates.append(year);

    else:
        for date in range(int(startDate), int(endDate) + 1):
            yearDates = str(year) + '.' + str(date)

            jq_comments = jq_comment_data[
                (jq_comment_data['data_website'] == platform) & (jq_comment_data[yearDate] == yearDates)];


            commentsValues.append(jq_comments.iloc[:, 0].size);
            if (round(jq_comments['comment_score'].mean() is np.nan)):
                gradesValues.append(0);
            else:
                gradesValues.append(round(jq_comments['comment_score'].mean(), 1));
            dates.append(date);

    return dates, commentsValues, gradesValues;
def isLeapYear(year):
    if(year % 400 == 0):
     return 1;
    elif(year % 100 != 0 and year % 4 == 0):
     return 1;
    else:
     return 0;
#所有平台上的总评论和总分 获取最近的动态
def getCommentsRecentState(time,platform,jq):
    #获取时间 返回值
    commentsValues = 0;
    gradesValues = 0;
    grades = 0;
    year = datetime.datetime.now().year;
    month = datetime.datetime.now().month;
    day = datetime.datetime.now().day;

    season = 0;
    yearDate = "";
    date = "";
    jq_comments = comments_data[
        (comments_data['data_source'] == '景点') & (comments_data['data_region'] == jq) & (
            comments_data['data_website'] == platform)];

    if(month % 3 == 0):
        season  = int(month / 3);
    else:
        season =  int(math.floor(month / 3) + 1);
    if(time == 'year'):
        #获取当前月与当前年份 比如当前月份是2018年5月 则截取时间为2017.5-2018.5

        for i in range(0,12):
            if(month > 1):
                month -= 1
            else:
                year -= 1
                month = 12;
            yearDate = str(year) + "." + str(month)



            jq_comments_vaules = jq_comments[(jq_comments['yearMonth'] == str(yearDate))];
            if (round(jq_comments_vaules['comment_score'].mean() is np.nan)):
                grades += 0;
            else:
                grades += (round(jq_comments['comment_score'].mean(), 1));
            commentsValues += jq_comments_vaules.iloc[:, 0].size;
        gradesValues = round(grades / 12,1);
    elif time == "season":

        for i in range(0,3):

                if (month > 1):
                    month -= 1
                else:
                    year -= 1
                    month = 12;

                yearDate = str(year) + "." + str(month)

                jq_comments_vaules = jq_comments[(jq_comments['yearMonth'] == str(yearDate))];
                if (round(jq_comments_vaules['comment_score'].mean() is np.nan)):
                  grades += 0;
                else:
                   grades += (round(jq_comments['comment_score'].mean(), 1));
                commentsValues += jq_comments_vaules.iloc[:, 0].size;
        gradesValues = round(grades / 3,1);
    elif time == "month":
        days = [[31,28,31,30,31,30,31,31,30,31,30,31],
                [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]];
        for i in range(0, 30):

                if (day > 1):
                    day -= 1
                else:
                    if (month > 1):
                        month -= 1
                        day = days[isLeapYear(year)][month - 1];
                    else:
                        year -= 1
                        month = 12;
                        day = 31;

                if(month < 10):
                 monthStr = str(0) + str(month);
                else:
                 monthStr = str(month);
                if(day < 10):
                 dayStr = str(0) + str(day);
                else:
                 dayStr = str(day);
                 yearDay = str(year) + "-" + monthStr + "-" + dayStr;

                 jq_comments_vaules = jq_comments[(jq_comments['day'] == str(yearDay))];
                 if (round(jq_comments_vaules['comment_score'].mean() is np.nan)):
                     grades += 0;
                 else:
                     grades += (round(jq_comments['comment_score'].mean(), 1));
                 commentsValues += jq_comments_vaules.iloc[:, 0].size;
        gradesValues = round(grades / 30,1);
    elif time == "week":
        days = [[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]];
        for i in range(0, 7):

            if (day > 1):
                day -= 1
            else:
                if (month > 1):
                    month -= 1
                    day = days[isLeapYear(year)][month - 1];
                else:
                    year -= 1
                    month = 12;
                    day = 31;

            if (month < 10):
                monthStr = str(0) + str(month);
            else:
                monthStr = str(month);
            if (day < 10):
                dayStr = str(0) + str(day);
            else:
                dayStr = str(day);
                yearDay = str(year) + "-" + monthStr + "-" + dayStr;

                jq_comments_vaules = jq_comments[(jq_comments['day'] == str(yearDay))];
                if (round(jq_comments_vaules['comment_score'].mean() is np.nan)):
                    grades += 0;
                else:
                    grades += (round(jq_comments['comment_score'].mean(), 1));
                commentsValues += jq_comments_vaules.iloc[:, 0].size;
        gradesValues = round(grades / 7,1);

    return  commentsValues,gradesValues;




def homepage(request):
    return render(request, 'InnerScenic.html');








'''
conn = mysql.connector.connect(host='10.1.17.25', user='repository', password='repository', database='repository')
client = pymongo.MongoClient('10.1.17.15',27017)
yilong_hotel_comments = pd.read_sql('select * from elong_comment;',con=conn)
yilong_hotel_shops = pd.read_sql('select * from elong_shop;',con=conn)
xiecheng_db = client['xiecheng_qiandaohu']
xiecheng_tb_comments = xiecheng_db['comments']
xiecheng_tb_shops = xiecheng_db['shops']
xiecheng_jingqu_comments = DataFrame(list(xiecheng_tb_comments.find()))
xiecheng_jingqu_shops = DataFrame(list(xiecheng_tb_shops.find()))
mafengwo_db = client['mafengwo_qiandaohu']
mafengwo_tb_comments = mafengwo_db['comments']
mafengwo_tb_shops = mafengwo_db['shops']
mafengwo_jingqu_comments = DataFrame(list(mafengwo_tb_comments.find()))
mafengwo_jingqu_shops = DataFrame(list(mafengwo_tb_shops.find()))
tuniu_db = client['tuniu_qiandaohu']
tuniu_tb_comments = tuniu_db['comments']
tuniu_tb_shops = tuniu_db['shops']
tuniu_jingqu_comments = DataFrame(list(tuniu_tb_comments.find()))
tuniu_jingqu_shops = DataFrame(list(tuniu_tb_shops.find()))
qunar_db = client['qunar_qiandaohu']
qunar_tb_comments = qunar_db['comments']
qunar_tb_shops = qunar_db['shops']
qunar_jingqu_comments = DataFrame(list(qunar_tb_comments.find()))
qunar_jingqu_shops = DataFrame(list(qunar_tb_shops.find()))
fliggy_db = client['fliggy_qiandaohu']
fliggy_tb_comments = fliggy_db['comments']
fliggy_tb_shops = fliggy_db['shops']
fliggy_jingqu_comments = DataFrame(list(fliggy_tb_comments.find()))
fliggy_jingqu_shops = DataFrame(list(fliggy_tb_shops.find()))
lvmama_db = client['lvmama_qiandaohu']
lvmama_tb_comments = lvmama_db['comments']
lvmama_tb_shops = lvmama_db['shops']
lvmama_jingqu_comments = DataFrame(list(lvmama_tb_comments.find()))
lvmama_jingqu_shops = DataFrame(list(lvmama_tb_shops.find()))
dianping_db = client['dianping_qiandaohu']
dianping_tb_comments = dianping_db['comments']
dianping_tb_shops = dianping_db['shops']
dianping_jingqu_comments = DataFrame(list(dianping_tb_comments.find()))
dianping_jingqu_shops = DataFrame(list(dianping_tb_shops.find()))
class All_ways():
    def __init__(self,data1,data2):
        self.comments = data1
        self.shops = data2
        self.comments['year'] = self.comments['comment_time'].apply(lambda x: int(x[0:4]))
        self.comments['month'] = self.comments['comment_time'].apply(lambda x: int(x[5:7]))
        self.comments['day'] = self.comments['comment_time'].apply(lambda x: x[0:10])
#每年评论数量的变化
    def get_year(self):
        a = self.comments['year'].value_counts().sort_index()
        indexlist = list(a.index)
        valuelist = list(a.values)
        return indexlist, valuelist
#总体上每个月评论数量的变化
    def get_month(self):
        a = self.comments['month'].value_counts().sort_index()
        indexlist = list(a.index)
        valuelist = list(a.values)
        return indexlist, valuelist
    def get_day(self):
        a = self.comments['day'].value_counts().sort_index()
        indexlist = list(a.index)
        valuelist = list(a.values)
        return indexlist, valuelist
#各年每个月评论数量的变化
    def get_year_month(self):
        year_month = {}
        a = self.comments.groupby(['year','month']).size().reset_index().rename(columns={0: 'count'})
        for i in range(len(a)):
            if a.iloc[i,0] not in year_month:
                year_month[a.iloc[i,0]] = {}
                year_month[a.iloc[i, 0]][a.iloc[i, 1]] = a.iloc[i, 2]
            elif a.iloc[i,0] in year_month and a.iloc[i,1] not in year_month[a.iloc[i,0]]:
                year_month[a.iloc[i,0]][a.iloc[i,1]] = a.iloc[i,2]
        return year_month
#景区按照评论数的topten
    def get_commenttopten(self):
        topten = self.shops.sort_values(by='shop_comment', ascending=False).head(10)
        return list(topten['shop_name'].values),list(topten['shop_comment'].values)
#景区价格分布
    def get_shop_price(self):
        pricelist = []
        price = ['0-100','100-200','200-300']
        for i in range(3):
            pricelist.append(len(self.shops[(self.shops['shop_price']<=(i+1)*100) & (self.shops['shop_price']>i*100)]))
        return price,pricelist
#景区最低价格分布
    def get_lowestPrice(self):
        lowestprice = ['0-50','50-100','100-150','150-200','200-250','250以上']
        pricelist = []
        for i in range(6):
            pricelist.append(len(self.shops[(self.shops['shop_price']<=(i+1)*50) & (self.shops['shop_price']>i*50)]))
        pricelist.append(len(self.shops[self.shops['shop_price']>250]))
        return lowestprice,pricelist
#景区按照评分的topten
    def get_scoretopten(self):
        a = self.shops[self.shops['shop_comment']>200]
        topten = a.sort_values(by='shop_grade',ascending=False).head(10)
        return list(topten['shop_name'].values),list(topten['shop_grade'].values)

    def get_score_month(self):
        score_month = {}
        b = self.comments.groupby(['year', 'month', 'comment_grade']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i, 0] not in score_month:
                score_month[b.iloc[i, 0]] = {}
                score_month[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in score_month and b.iloc[i, 1] not in score_month[b.iloc[i, 0]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in score_month and b.iloc[i, 1] in score_month[b.iloc[i, 0]] and b.iloc[i, 2] not in \
                    score_month[b.iloc[i, 0]][b.iloc[i, 1]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return score_month
    def get_score_day(self):
        score_day = {}
        b = self.comments.groupby(['day','comment_grade']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i,0] not in score_day:
                score_day[b.iloc[i,0]] = {}
                score_day[b.iloc[i,0]][b.iloc[i,1]] = b.iloc[i,2]
            elif b.iloc[i,0] in score_day and b.iloc[i,1] not in score_day[b.iloc[i,0]]:
                score_day[b.iloc[i,0]][b.iloc[i,1]] = b.iloc[i,2]
        return score_day


#艺龙的酒店评星有点问题很多都是0
class Yilong_hotel_way(All_ways):
    def __init__(self,data1,data2):
        self.comments = data1
        self.shops = data2
        self.comments['year'] = self.comments['commentDateTime'].apply(lambda x: int(x[0:4]))
        self.comments['month'] = self.comments['commentDateTime'].apply(lambda x: int(x[5:7]))
        self.comments['day'] = self.comments['commentDateTime'].apply(lambda x: x[0:10])
        self.comments['commentScoreTotal'] = self.comments['commentScoreTotal'].apply(self.change)
    @staticmethod
    def change(words):
        if words == 1 or words == 2:
            words = "差评"
        elif words == 3 or words == 4:
            words = "中评"
        elif words == 5:
            words = "好评"
        else:
            words = words
        return words
    #酒店所在区域
    def get_areacount(self):
        a = self.shops['businessAreaName'].value_counts()
        indexlist = list(a.index)
        valuelist = list(a.values)
        indexlist.pop()
        valuelist.pop()
        return indexlist,valuelist
    @staticmethod
    def getdistance(words):
        if words is None:
            return 1000
        if len(words)<17:
            return 0.1
        re_word = re.compile('(\w{5})(\d{0,4}.\d{0,4})(\w{2}),(\w{4})(\d{0,4}.\d{0,4})(\w{2}),(\w)(\d{1,2})(\w{2})')
        handleword = re_word.match(words)
        return float(handleword.group(2))
    @staticmethod
    def gettime(words):
        if words is None:
            return 1000
        if len(words)<17:
            return 0
        re_word = re.compile('(\w{5})(\d{0,4}.\d{0,4})(\w{2}),(\w{4})(\d{0,4}.\d{0,4})(\w{2}),(\w)(\d{1,2})(\w{2})')
        handleword = re_word.match(words)
        return float(handleword.group(8))
    #酒店离景区的距离
    def get_distancetime(self):
        distancelist = []
        distancevalues = ['0-2公里','2-４公里','4公里以上']
        self.shops['distance'] = self.shops['trafficInfo'].apply(self.getdistance)
        for i in range(3):
            distancelist.append(len(self.shops[(self.shops['distance']<=(i+1)*2) & (self.shops['distance']>i*2)]))
        return distancevalues,distancelist
    #酒店去景区的时间
    def get_time(self):
        timelist = []
        timevalue = ['0-5分钟','5-10分钟','10分钟以上']
        self.shops['time'] = self.shops['trafficInfo'].apply(self.gettime)
        for i in range(3):
            timelist.append(len(self.shops[(self.shops['time']<=(i+1)*5) & (self.shops['time']>i*5)]))
        return timevalue,timelist
    #根据评论数量排的top10
    def get_commenttopten(self):
        topten = self.shops.sort_values(by='totalCommentCount', ascending=False).head(10)
        return list(topten['hotelName'].values),list(topten['totalCommentCount'].values)
    #根据酒店评分排的top10
    def get_scoretopten(self):
        a = self.shops[self.shops['totalCommentCount']>200]
        topten = a.sort_values(by='commentScore',ascending=False).head(10)
        return list(topten['hotelName'].values),list(topten['commentScore'].values)
    #酒店最低价的分布情况
    def get_lowestPrice(self):
        lowestprice = ['0-200','200-400','400-600','600-800','800-1000','1000以上']
        pricelist = []
        for i in range(6):
            pricelist.append(len(self.shops[(self.shops['lowestPrice']<=(i+1)*200) & (self.shops['lowestPrice']>i*200)]))
        pricelist.append(len(self.shops[self.shops['lowestPrice']>1000]))
        return lowestprice,pricelist
    #酒店评分每个月的变化
    def get_score_month(self):
        score_month = {}
        a = self.comments.groupby(['year', 'month', 'commentScoreTotal']).size().reset_index().rename(
            columns={0: 'count'})
        b = a[a['commentScoreTotal']!=0]
        for i in range(len(b)):
            if b.iloc[i,0] not in score_month:
                score_month[b.iloc[i,0]] = {}
                score_month[b.iloc[i,0]][b.iloc[i,1]]={}
                score_month[b.iloc[i,0]][b.iloc[i,1]][b.iloc[i,2]] = b.iloc[i,3]
            elif b.iloc[i,0] in score_month and b.iloc[i,1] not in score_month[b.iloc[i,0]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_month[b.iloc[i,0]][b.iloc[i,1]][b.iloc[i,2]] = b.iloc[i,3]
            elif b.iloc[i,0] in score_month and b.iloc[i,1] in score_month[b.iloc[i,0]] and b.iloc[i,2] not in score_month[b.iloc[i,0]][b.iloc[i,1]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return score_month
    def get_score_day(self):
        score_day = {}
        a = self.comments.groupby(['day','commentScoreTotal']).size().reset_index().rename(
            columns={0: 'count'})
        b = a[a['commentScoreTotal'] != 0]
        for i in range(len(b)):
            if b.iloc[i,0] not in score_day:
                score_day[b.iloc[i,0]] = {}
                score_day[b.iloc[i,0]][b.iloc[i,1]] = b.iloc[i,2]
            elif b.iloc[i,0] in score_day and b.iloc[i,1] not in score_day[b.iloc[i,0]]:
                score_day[b.iloc[i,0]][b.iloc[i,1]] = b.iloc[i,2]
        return score_day
class Xiecheng_jingqu_way(All_ways):
    def __init__(self,data1,data2):
        self.comments = data1
        self.shops = data2
        self.comments['year'] = self.comments['comment_time'].apply(lambda x: int(x[0:4]))
        self.comments['month'] = self.comments['comment_time'].apply(lambda x: int(x[5:7]))
        self.comments['day'] = self.comments['comment_time'].apply(lambda x: x[0:10])
        self.comments['comment_grade'] = self.comments['comment_grade'].apply(self.change)
    @staticmethod
    def change(words):
        if int(words[0]) == 1 or int(words[0]) == 2:
            words = "差评"
        elif int(words[0]) == 3 or int(words[0]) == 4:
            words = "中评"
        else:
            words = "好评"
        return words
#马蜂窝的价格有点问题
class Mafengwo_jingqu_way(All_ways):
    def __init__(self,data1,data2):
        self.comments = data1
        self.shops = data2
        self.comments['comment_time'] = self.comments['comment_time'].apply(self.convert_time)
        self.comments['year'] = self.comments['comment_time'].apply(lambda x: int(x[0:4]))
        self.comments['month'] = self.comments['comment_time'].apply(lambda x: int(x[5:7]))
        self.comments['day'] = self.comments['comment_time'].apply(lambda x: x[0:10])
    @staticmethod
    def convert_time(words):
        if len(words)<=5:
            return time.strftime('%Y-%m-%d',time.localtime(time.time()))
        else:
            return words
class Tuniu_jingqu_way(All_ways):
    def __init__(self,data1,data2):
        self.comments = data1
        self.shops = data2
        self.comments['year'] = self.comments['comment_time'].apply(lambda x: int(x[0:4]))
        self.comments['month'] = self.comments['comment_time'].apply(lambda x: int(x[5:7]))
        self.comments['day'] = self.comments['comment_time'].apply(lambda x: x[0:10])
        self.comments['yuding'] = self.comments['comment_evaluation'].apply(self.get_yuding)
        self.comments['qupiao'] = self.comments['comment_evaluation'].apply(self.get_qupiao)
        self.comments['fuwu'] = self.comments['comment_evaluation'].apply(self.get_fuwu)
    @staticmethod
    def get_yuding(words):
        if len(words)>0:
            if words[0]['showGradeValue']=='满意':
                return '好评'
            elif words[0]['showGradeValue']=='一般':
                return '中评'
            else:
                return '差评'
        else:
            return 0
    @staticmethod
    def get_qupiao(words):
        if len(words)==3:
            if words[0]['showGradeValue']=='满意':
                return '好评'
            elif words[0]['showGradeValue']=='一般':
                return '中评'
            else:
                return '差评'
        else:
            return 0
    @staticmethod
    def get_fuwu(words):
        if len(words)==3:
            if words[2]['showGradeValue']=='满意':
                return '好评'
            elif words[2]['showGradeValue']=='一般':
                return '中评'
            else:
                return '差评'
        elif len(words)==2:
            if words[1]['showGradeValue']=='满意':
                return '好评'
            elif words[1]['showGradeValue']=='一般':
                return '中评'
            else:
                return '差评'
        else:
            return 0
    def get_yuding_month(self):
        score_month = {}
        b = self.comments.groupby(['year', 'month', 'yuding']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i,0] not in score_month:
                score_month[b.iloc[i,0]] = {}
                score_month[b.iloc[i,0]][b.iloc[i,1]]={}
                score_month[b.iloc[i,0]][b.iloc[i,1]][b.iloc[i,2]] = b.iloc[i,3]
            elif b.iloc[i,0] in score_month and b.iloc[i,1] not in score_month[b.iloc[i,0]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_month[b.iloc[i,0]][b.iloc[i,1]][b.iloc[i,2]] = b.iloc[i,3]
            elif b.iloc[i,0] in score_month and b.iloc[i,1] in score_month[b.iloc[i,0]] and b.iloc[i,2] not in score_month[b.iloc[i,0]][b.iloc[i,1]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return score_month
    def get_qupiao_month(self):
        score_month = {}
        b = self.comments.groupby(['year', 'month', 'qupiao']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i,0] not in score_month:
                score_month[b.iloc[i,0]] = {}
                score_month[b.iloc[i,0]][b.iloc[i,1]]={}
                score_month[b.iloc[i,0]][b.iloc[i,1]][b.iloc[i,2]] = b.iloc[i,3]
            elif b.iloc[i,0] in score_month and b.iloc[i,1] not in score_month[b.iloc[i,0]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_month[b.iloc[i,0]][b.iloc[i,1]][b.iloc[i,2]] = b.iloc[i,3]
            elif b.iloc[i,0] in score_month and b.iloc[i,1] in score_month[b.iloc[i,0]] and b.iloc[i,2] not in score_month[b.iloc[i,0]][b.iloc[i,1]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return score_month
    def get_fuwu_month(self):
        score_month = {}
        b = self.comments.groupby(['year', 'month', 'fuwu']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i,0] not in score_month:
                score_month[b.iloc[i,0]] = {}
                score_month[b.iloc[i,0]][b.iloc[i,1]]={}
                score_month[b.iloc[i,0]][b.iloc[i,1]][b.iloc[i,2]] = b.iloc[i,3]
            elif b.iloc[i,0] in score_month and b.iloc[i,1] not in score_month[b.iloc[i,0]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_month[b.iloc[i,0]][b.iloc[i,1]][b.iloc[i,2]] = b.iloc[i,3]
            elif b.iloc[i,0] in score_month and b.iloc[i,1] in score_month[b.iloc[i,0]] and b.iloc[i,2] not in score_month[b.iloc[i,0]][b.iloc[i,1]]:
                score_month[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return score_month
class Qunar_jingqu_way(All_ways):
    def __init__(self,data1,data2):
        self.comments = data1
        self.shops = data2
        self.comments['year'] = self.comments['comment_time'].apply(lambda x: int(x[0:4]))
        self.comments['month'] = self.comments['comment_time'].apply(lambda x: int(x[5:7]))
        self.comments['day'] = self.comments['comment_time'].apply(lambda x: x[0:10])
        self.comments['comment_grade'] = self.comments['comment_grade'].apply(self.change)
    @staticmethod
    def change(words):
        if words == 1 or words == 2:
            words = "差评"
        elif words == 3 or words == 4:
            words = "中评"
        elif words == 5:
            words = "好评"
        else:
            words = words
        return words
class Fliggy_jingqu_way(All_ways):
    
    def get_star(self):
        a = self.shops['shop_rate'].value_counts()
        indexlist = list(a.index)
        valuelist = list(a.values)
        indexlist.pop(0)
        valuelist.pop(0)
        return indexlist, valuelist

class Lvmama_jingqu_way(All_ways):
    pass
class Dianping_jingqu_way(All_ways):
    def __init__(self, data1, data2):
        self.comments = data1
        self.shops = data2
        self.comments['year'] = self.comments['comment_time'].apply(self.change_year)
        self.comments['month'] = self.comments['comment_time'].apply(self.change_month)
        self.comments['day'] = self.comments['comment_time'].apply(self.change_day)
    @staticmethod
    def change_year(words):
        if words is np.nan:
            return 1000
        else:
            return int(words[0:4])
    @staticmethod
    def change_month(words):
        if words is np.nan:
            return 1000
        else:
            return int(words[5:7])
    @staticmethod
    def change_day(words):
        if words is np.nan:
            return 1000
        else:
            return words[0:10]

class alljingqu():
    def __init__(self, data1, data2):
        data2 = data2[data2['shop_comment']!=0]
        self.shops = data2
        self.all = pd.merge(data2, data1, 'left', on=['shop_url'])
        self.all['year'] = self.all['comment_time'].apply(lambda x: int(x[0:4]))
        self.all['month'] = self.all['comment_time'].apply(lambda x: int(x[5:7]))
        self.all['day'] = self.all['comment_time'].apply(lambda x: x[0:10])
        self.jingqu_name = self.all['shop_name_x'].value_counts().index
  
    def get_year(self):
        all = {}
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]] = []
            #yield  jingqu_name[i]
            a = self.all[self.all['shop_name_x']==self.jingqu_name[i]]
            b = a['year'].value_counts().sort_index()
            all[self.jingqu_name[i]].append(list(b.index))
            all[self.jingqu_name[i]].append(list(b.values))
            #yield list(b.index)
            #yield list(b.values)
        return all
    def get_month(self):
        all = {}
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]] = []
            # yield  jingqu_name[i]
            a = self.all[self.all['shop_name_x'] == self.jingqu_name[i]]
            b = a['month'].value_counts().sort_index()
            all[self.jingqu_name[i]].append(list(b.index))
            all[self.jingqu_name[i]].append(list(b.values))
            # yield list(b.index)
            # yield list(b.values)
        return all
    def get_day(self):
        all = {}
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]] = []
            # yield  jingqu_name[i]
            a = self.all[self.all['shop_name_x'] == self.jingqu_name[i]]
            b = a['day'].value_counts().sort_index()
            all[self.jingqu_name[i]].append(list(b.index))
            all[self.jingqu_name[i]].append(list(b.values))
            # yield list(b.index)
            # yield list(b.values)
        return all
    def get_message(self):
        all = {}
        for i in range(len(self.jingqu_name)):
            all[self.jingqu_name[i]]=[]
            a = self.shops[self.shops['shop_name_x']==self.jingqu_name[i]]
            all[self.jingqu_name[i]].append(a['shop_name_x'].iloc[0])
            all[self.jingqu_name[i]].append(a['shop_address'].iloc[0])
            all[self.jingqu_name[i]].append(a['shop_feature'].iloc[0])
            all[self.jingqu_name[i]].append(a['shop_time'].iloc[0])
        return all
    def get_score_message(self):
        score_message = {}
        b = self.all.groupby(['shop_name_x', 'day', 'comment_grade']).size().reset_index().rename(
            columns={0: 'count'})
        for i in range(len(b)):
            if b.iloc[i, 0] not in score_message:
                score_message[b.iloc[i, 0]] = {}
                score_message[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_message[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in score_message and b.iloc[i, 1] not in score_message[b.iloc[i, 0]]:
                score_message[b.iloc[i, 0]][b.iloc[i, 1]] = {}
                score_message[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
            elif b.iloc[i, 0] in score_message and b.iloc[i, 1] in score_message[b.iloc[i, 0]] and b.iloc[i, 2] not in score_message[b.iloc[i, 0]][b.iloc[i, 1]]:
                score_message[b.iloc[i, 0]][b.iloc[i, 1]][b.iloc[i, 2]] = b.iloc[i, 3]
        return score_message

yilong_hotel = Yilong_hotel_way(yilong_hotel_comments,yilong_hotel_shops)
xiecheng_jingqu = Xiecheng_jingqu_way(xiecheng_jingqu_comments,xiecheng_jingqu_shops)
mafengwo_jingqu = Mafengwo_jingqu_way(mafengwo_jingqu_comments,mafengwo_jingqu_shops)
tuniu_jingqu = Tuniu_jingqu_way(tuniu_jingqu_comments,tuniu_jingqu_shops)
qunar_jingqu = Qunar_jingqu_way(qunar_jingqu_comments,qunar_jingqu_shops)
fliggy_jingqu = Fliggy_jingqu_way(fliggy_jingqu_comments,fliggy_jingqu_shops)
lvmama_jingqu = Lvmama_jingqu_way(lvmama_jingqu_comments,lvmama_jingqu_shops)
dianping_jingqu = Dianping_jingqu_way(dianping_jingqu_comments,dianping_jingqu_shops)
all_jingqu = alljingqu(xiecheng_jingqu_comments,xiecheng_jingqu_shops)
def index2(request):
    return render(request,'all.html')
def all(request):
    date = []
    haoping = []
    zhongping = []
    chaping = []
    year = request.POST['year']
    month = request.POST['month']
    dict = qunar_jingqu.get_score_month()
    dict2 = qunar_jingqu.get_score_day()
    list5 = sorted(dict2.items(), key=lambda d: d[0])
    for i, j in enumerate(list5):
        if j[0][0:4] == year and j[0][5:7] == month:
            date.append(j[0])
            j[1].setdefault('差评', 0)
            j[1].setdefault('中评', 0)
            j[1].setdefault('好评', 0)
            haoping.append(j[1]['好评'])
            zhongping.append(j[1]['中评'])
            chaping.append(j[1]['差评'])
    a = sorted(dict.items(), key=lambda d: d[0])
    print(a)
    if int(year) not in dict or int(month) not in dict[int(year)]:
        return render(request,'all.html',{
            'jianyan':'该数据不存在！',
        })
    list3 = ['差评','中评','好评']
    list4=[]
    for i in list3:
        dict[int(year)][int(month)].setdefault(i,0)
        list4.append(dict[int(year)][int(month)][i])
    print(list4)
    list1,list2 = qunar_jingqu.get_year()
    return render(request,'all.html',{
        'list1':json.dumps(list1),
        'list2':list2,
        'list3': date,
        'list4': chaping,
        'list5': zhongping,
        'list6': haoping,
    })
def index(request):
    return render(request,'data.html')
def data(request):
    name = request.POST['name']
    year = request.POST['year']
    month = request.POST['month']
    date = []
    haoping = []
    zhongping = []
    chaping = []
    dict = all_jingqu.get_month()
    dict2 = all_jingqu.get_message()
    list3 = dict2[name]
    #list1 = dict[name][0]
    #list2 = dict[name][1]
    dict3 = all_jingqu.get_day()
    list1 = dict3[name][0][-15:] #只取最近15天的数据
    list2 = dict3[name][1][-15:]
    dict4 = all_jingqu.get_score_message()
    list4 = sorted(dict4[name].items(),key=lambda d:d[0])
    for i,j in enumerate(list4):
        if j[0][0:4]==year and j[0][5:7]==month:
            date.append(j[0])
            j[1].setdefault('差评',0)
            j[1].setdefault('中评',0)
            j[1].setdefault('好评',0)
            haoping.append(j[1]['好评'])
            zhongping.append(j[1]['中评'])
            chaping.append(j[1]['差评'])
    return render(request, 'data.html', {
        'name': json.dumps(name),
        'list1': json.dumps(list1),
        'list2': list2,
        'message': list3,
        'list3':date,
        'list4':chaping,
        'list5':zhongping,
        'list6':haoping,
        })
'''