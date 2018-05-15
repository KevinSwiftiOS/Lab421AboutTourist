$("#tijiao").click(function () {
    
    var year = $("#year").val();
    var month = [];
    var pingtai = [];
    var name = $("#name").val();
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
    var errorMes = "";
    if(name == "")
      errorMes += "景区名字未填";
     if(month.length == 0)
     errorMes += "未选择月份";
     if(pingtai.length == 0)
     errorMes += "未选择平台";
     if(errorMes != "")
     swal("提醒",errorMes,"warning");
     else{
        $.LoadingOverlay("show"); 
    var param = {
        'pingtai':JSON.stringify(pingtai),
        'year':year,
        'month':JSON.stringify(month),
        'name':$("#name").val()
    };
    console.log(param);
    $.ajax({
            headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
            url:"/kindjq",
            type:"POST",
            data:param,
            success:function (data) {
                $.LoadingOverlay("hide"); 
                if(data.code == 0){
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
                         data: data["monthIndexs"]
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
                         data:data["monthValues"]
                     }]
                 };
                 var option1 = {
                     tooltip: {},
                     legend: {
                         data:[]
                     },
                     xAxis: {
                         name: '年份',
                         data: data["yearIndexs"]
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
                         data: data["yearValues"]
                     }]
                 };
                 var option2 = {
                     tooltip: {},
                     legend: {
                         data:[]
                     },
                     xAxis: {
                         name:'最近四周',
                         data: data["weekIndexs"]
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
                         data: data["weekValues"]
                     }]
                 };
                 var option3 = {
                     tooltip: {},
                     legend: {
                         data:[]
                     },
                     xAxis: {
                         name:'最近15天',
                         data: data["dayIndexs"]
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
                         data: data["dayValues"]
                     }]
                 };
                 myChartone.setOption(option);
                 myCharttwo.setOption(option1);
                 myChartthree.setOption(option2);
                 myChartfour.setOption(option3);
    
                }else{
                    swal("请求失败",data.message,"error");
                }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    },
            error:function () {
                $.LoadingOverlay("hide"); 
              swal("请求失败","请尝试再次请求","error");

            }
        });
    }
        return false;
    
    });