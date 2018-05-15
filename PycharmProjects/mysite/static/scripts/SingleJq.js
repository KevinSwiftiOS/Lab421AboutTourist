
var Item = function () {
    return {
        name: '',
        type: 'line',
        data: []
    }
};
var gradesItem = function () {
    return {
        name: '',
        type: 'bar',
        data: []
    }
};
$("#submit").click(function () {
     
 
    var jqs = [];
    var  platforms = [];
    //开始与结束月份获取
    var startYear = $("#startYear").val();   
    var startDate = $("#startMonth").val();   
    var endYear = $("#endYear").val();   
    var endDate = $("#endMonth").val();   
    var  time = $("#time").val();
    //景区获取

   
   
     jgObj = document.getElementsByName("jq");
    for (i in jgObj) {
        if (jgObj[i].checked)
        jqs.push(jgObj[i].value);
    }
    platformObj = document.getElementsByName("platform");
    for (i in platformObj) {
        if (platformObj[i].checked)
            platforms.push(platformObj[i].value);
    }

    var errMes = "";
    if(jqs.length == 0)
    errMes += "未选择景区"
    if(platforms.length == 0)
      errMes += "未选择平台";
    if(errMes != "")
    swal("提醒",errMes,"warning");  
    
    else {
        $.LoadingOverlay("show");
    var param = {
        'jqs': JSON.stringify(jqs),
        'startYear':startYear,
        'endYear':endYear,
        'startDate':startDate,
        'endDate':endDate,
        'platforms':JSON.stringify(platforms),
        'time':time
    };
    console.log(param);
    $.ajax({
        headers: { "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').val() },
        url: "/singlejq",
        type: "POST",
        data: param,
        success: function (res) {
            $("#echart").empty();
            $.LoadingOverlay("hide");
            if(res.code == 0){
            var data = res.data;
            console.log(data);
            for(var i = 0; i < data.jqs.length;i++){

            var commentOption = {
                title:{
                    text:data.jqs[i].jq + "在不同平台上评论数量的变化"
                },
                tooltip:{
                    trigger:"axis"
                },
                //折现有几条
                legend:{
                    data:[]
                },
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : data.dates
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                        axisLabel : {
                            formatter: '{value}'
                        }
                    }
                ],
                series: [],
            };
            var gradeOption = {
                title:{
                    text:data.jqs[i].jq + "在不同平台上评分的变化"
                },
                tooltip:{
                    trigger:"axis"
                },
                //折现有几条
                legend:{
                    data:[]
                },
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : data.dates
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                        axisLabel : {
                            formatter: '{value}'
                        }
                    }
                ],
                series: [],
            }
                for(var j = 0; j < data.jqs[i].platforms.length;j++){
                    var platform =  data.jqs[i].platforms[j];
                    console.log(platform);
                    commentOption.legend.data.push(platform.name);
                    gradeOption.legend.data.push(platform.name);
                        var commentItem = new Item();
                        commentItem.name = platform.name;
                        commentItem.data = platform.commentValue;
                        commentOption.series.push(commentItem);
                        var gradeItem = new Item();
                        gradeItem.name = platform.name;
                        gradeItem.data = platform.gradeValue;
                        gradeOption.series.push(gradeItem);
                    
                }
                var commentDiv = '<div id=' + "'" +data.jqs[i].jq + "评论" + "'" + ' style="width: 500px;height:400px;float:left"></div>'
                var gradeDiv = '<div id=' + "'" +data.jqs[i].jq + "评分" + "'" + ' style="width: 500px;height:400px;float:left"></div>'
             
                $("#echart").append(commentDiv);
                $("#echart").append(gradeDiv);
                var commentChart = echarts.init(document.getElementById( data.jqs[i].jq + "评论"));
                commentChart.setOption(commentOption, true);
                var gradeChart = echarts.init(document.getElementById( data.jqs[i].jq + "评分"));
                gradeChart.setOption(gradeOption, true);
            }
            }




        //    if(data.code == 0) {
        //     var jqText = "";
        //     for(var i = 0; i < jq.length;i++)
        //     jqText += jq[i] + ",";
       
        //    var monthText = year + "年";
        //    for(var i = 0; i < month.length;i++)
        //    monthText += month[i] + ",";
        //    monthText += "月";
        //    if(jq.length > 1) {
        //    $("#commentsP").text(jqText + year + "年的评论数量比较");
        //    $("#gGradesP").text(jqText + monthText + "年的好评等级数量比较");
        //    $("#mGradesP").text(jqText + monthText + "年的中评等级数量比较");
        //    $("#bGradesP").text(jqText + monthText + "年的差评等级数量比较");

        //    }
        //    else{
        //    $("#commentsP").text(jqText + year + "年的评论数量变化");
        //    $("#gGradesP").text(jqText + monthText + "年的好评等级数量变化");
        //    $("#mGradesP").text(jqText + monthText + "年的中评等级数量比较");
        //    $("#bGradesP").text(jqText + monthText + "年的差评等级数量比较");


        //    }
          
        //     console.log(data);
        //     var commentsChart = echarts.init(document.getElementById('commentsDiv'));
        //     var gGradesChart = echarts.init(document.getElementById('gGradesDiv'));
        //     var mGradesChart = echarts.init(document.getElementById('mGradesDiv'));
        //     var bGradesChart = echarts.init(document.getElementById('bGradesDiv'));
        //     var commentsSeries = [];
        //     for (var i = 0; i < jq.length; i++) {
        //         var it = new Item();
        //         it.name = jq[i];
        //         it.data = data[jq[i]]['month_number'];
        //         commentsSeries.push(it);
        //     }
        //     var commentsOptions = {
        //         tooltip: {
        //             trigger: 'axis'
        //         },
        //         legend: {
        //             data: jq
        //         },
        //         xAxis: {
        //             type: 'category',
        //             boundaryGap: false,
        //             data: data[jq[0]]['month']
        //         },
        //         yAxis: {
        //             type: 'value',
        //             axisLabel: {
        //                 formatter: '{value}'
        //             }
        //         },
        //         series: []
        //     };
        //     console.log(commentsSeries);
        //     commentsOptions.series = commentsSeries;
            
        //     commentsChart.setOption(commentsOptions, true);
        //    //好评数的变化
        //     var gGradesOptions = initOptions('haoping',data);
        //     gGradesChart.setOption(gGradesOptions,true);

        //     var mGradesOptions = initOptions('zhongping',data);
        //     mGradesChart.setOption(mGradesOptions,true);
        //     var bGradesOptions = initOptions('chaping',data);
        //     bGradesChart.setOption(bGradesOptions,true);
        // }else{
        //     swal("提醒",data.message,"error");
        // }













        },
        error: function (error) {
            $.LoadingOverlay("hide");
            swal("请求失败", "请尝试再次请求", "error");

        }
    }
    )
}

    return false;

}
);
//初始化option
function initOptions(grades,data) {
var Series = [];
for(var i = 0; i < jq.length;i++){
    var it = new gradesItem();
    it.name = jq[i];
    it.data = data[jq[i]][grades];
    Series.push(it);
}
var options = {
 tooltip: {
     trigger: 'axis'
 },
 legend: {
     data: jq
 },
 xAxis: {
     type: 'category',
 
     data: data[jq[0]]['gradeMonths']
 },
 yAxis: {
     type: 'value',
     axisLabel: {
         formatter: '{value}'
     }
 },
 series: []
};
options.series = Series;
 return options;
}