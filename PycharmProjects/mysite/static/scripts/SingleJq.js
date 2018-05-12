
//应该通过与ajax交互
$(document).ready(function () {
   
});

$("#submit").click(function () {

    //获取各个时间节点
    var name = $("#name").val();
    var startYear = $("#startYear").val();
    var startMonth = $("#startMonth").val();
    var endYear = $("#endYear").val();
    var endMonth = $("#endMonth").val();
    var time = $("#time").val();
    //错误信息 都为必填字段
    var errorMes = "";
    if (name == null || name == "")
        errorMes += "景区名字未填,";
    if (startYear == null || startMonth == null || endYear == null || endMonth == null)
        errorMes += "开始与结束年月份未选择完全";

    if (time == undefined || time == "")
        errorMes += "未选择期限";
    if (errorMes != "")
        swal("提醒", errorMes, "warning");

    else {
        //$("#main1P").text(year + "年" + month + "月" + "评论等级变化情况：");
        $("#mainP").text(startYear + "年" + startMonth + "月至" + endYear + "年" + endMonth + "月评论变化情况");
        //进行ajax交互
        $.LoadingOverlay("show");
        var param = {
            name: $("#name").val(),
            startYear: $("#startYear").val(),
            startMonth: $("#startMonth").val(),
            endYear: $("#endYear").val(),
            endMonth: $("#endMonth").val(),
            time: $("#time").val()
        };

        $.ajax({
            headers: { "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').val() },
            url: "/singlejq",
            type: "POST",
            data: { "param": JSON.stringify(param) },
            success: function (data) {
                $.LoadingOverlay("hide");
                console.log(data.xAxis);
                if (data.success) {
                    var message = data.message;
                    var tbody = "";
                    //首先message元素的所有子元素
                    $("#meassage").empty();
                    $.each(message, function (key, value) {
                        //景区信息
                        var trs = "";
                        trs += " <p> " + key + " </p> <p>" + value + "</p>";
                        tbody += trs;
                    });
                    $("#meassage").append(tbody);
                    //绘制图表
                    var colors = ['#5793f3', '#d14a61', '#675bba'];
                    var myChart = echarts.init(document.getElementById('main'));
                    var myChartone = echarts.init(document.getElementById('main1'));
                    var option = {
                        tooltip: {},
                        legend: {
                            data: []
                        },
                        xAxis: {
                            data: data.xAxis
                        },
                        yAxis: {
                          
                        },
                        series: [{
                            name: '',
                            type: 'bar',
                            data: data.yAxis
                        }]
                    };
                    var option1 = {
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {
                            data: ['差评数', '中评数', '好评数']
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: data.date
                        },
                        yAxis: {
                            type: 'value',
                            axisLabel: {
                                formatter: '{value}'
                            }
                        },
                        series: [
                            {
                                name: '差评数',
                                type: 'line',
                                data: data.chaping
                            },
                            {
                                name: '中评数',
                                type: 'line',
                                data: data.zhongping
                            },
                            {
                                name: '好评数',
                                type: 'line',
                                data: data.haoping
                            }
                        ]
                    };
                    myChart.setOption(option);
                    myChartone.setOption(option1);
                } else {
                    swal("请求失败", data.error, "warning");
                }
            },
            error: function (error) {
                $.LoadingOverlay("hide");
                swal("请求失败", "请尝试再次刷新", "error");
            }
        })
    }
    return false;









}
);

