$("#tijiao").click(function () {
    var year = $("#year").val();
    var month = [];
    var pingtai = [];
    var myChartsix;
    obj1 = document.getElementsByName("month");
    for(k in obj1) {
        if (obj1[k].checked)
            month.push(obj1[k].value);
    }
    obj2 = document.getElementsByName("pingtai");
    for(k in obj2) {
        if (obj2[k].checked)
            pingtai.push(obj2[k].value);
    }
    $.ajax({
            headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
            url:"/kindjq",
            type:"POST",
            data:{'pingtai':JSON.stringify(pingtai),'year':year,'month':JSON.stringify(month)},
            success:function (data) {
                var Item = function () {
                    return {
                        name:'',
                        type:'line',
                        data:[]
                    }
                };
                var myChartfive = echarts.init(document.getElementById('result1'));
                var Series = [];
                for(var i=0;i<pingtai.length;i++){
                    var it = new Item();
                    it.name = pingtai[i];
                    it.data = data['month_number'][i];
                    Series.push(it);
                }
                 myChartsix = echarts.init(document.getElementById('result2'));
               var option4 = {
                   tooltip: {
    trigger: 'axis',
    axisPointer: {
        type: 'cross',
        crossStyle: {
            color: '#999'
        }
    }
},
legend: {
    data:['差评','中评','好评']
},
xAxis: [
    {
        type: 'category',
        data: month,
        axisPointer: {
            type: 'shadow'
        }
    }
],
yAxis: [
    {
        type: 'value',
        name: '数量',
        axisLabel: {
            formatter: '{value}'
        }
    }
],
series: [
    {
        name:'好评',
        type:'bar',
        data:data['haoping']
    },
    {
        name:'中评',
        type:'bar',
        data:data['zhongping']
    },
    {
        name:'差评',
        type:'bar',
        data:data['chaping']
    },
]
};
       myChartfive.setOption(option4,true);


        var option5 = {
tooltip: {
    trigger: 'axis'
},
legend: {
    data:pingtai
},
xAxis:  {
    type: 'category',
    boundaryGap: false,
    data: data['month']
},
yAxis: {
    type: 'value',
    axisLabel: {
        formatter: '{value}'
    }
},
series: []
};
        option5.series = Series;
        myChartsix.setOption(option5,true);
            },
            error:function () {
                alert('error')

            }
        });
        return false;
    });
    var colors = ['#5793f3', '#d14a61', '#675bba'];
    var myChartone = echarts.init(document.getElementById('main1'));
    var myCharttwo = echarts.init(document.getElementById('main2'));
    var myChartthree = echarts.init(document.getElementById('main3'));
    var myChartfour = echarts.init(document.getElementById('main4'));
    var option = {
        tooltip: {},
        legend: {
            data:[]
        },
        xAxis: {
            name: '月份',
            data: {{list1|safe}}
        },
        yAxis: {
        type: 'value',
        name: '数量',
        axisLabel: {
            formatter: '{value}'
        }

        },
        series: [{
            name: '数量',
            type: 'bar',
            data: {{list2|safe}}
        }]
    };
    var option1 = {
        tooltip: {},
        legend: {
            data:[]
        },
        xAxis: {
            name: '年份',
            data: {{list3|safe}}
        },
        yAxis: {
        type: 'value',
        name: '数量',
        axisLabel: {
            formatter: '{value}'
        }

        },
        series: [{
            name: '数量',
            type: 'bar',
            data: {{list4|safe}}
        }]
    };
    var option2 = {
        tooltip: {},
        legend: {
            data:[]
        },
        xAxis: {
            name:'最近四周',
            data: {{list5|safe}}
        },
        yAxis: {
        type: 'value',
        name: '数量',
        axisLabel: {
            formatter: '{value}'
        }

        },
        series: [{
            name: '数量',
            type: 'bar',
            data: {{list6|safe}}
        }]
    };
    var option3 = {
        tooltip: {},
        legend: {
            data:[]
        },
        xAxis: {
            name:'最近15天',
            data: {{list7|safe}}
        },
        yAxis: {
        type: 'value',
        name: '数量',
        axisLabel: {
            formatter: '{value}'
        }

        },
        series: [{
            name: '数量',
            type: 'bar',
            data: {{list8|safe}}
        }]
    };
    myChartone.setOption(option);
    myCharttwo.setOption(option1);
    myChartthree.setOption(option2);
    myChartfour.setOption(option3);