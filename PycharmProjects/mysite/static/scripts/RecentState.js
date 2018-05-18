var Item = function () {
    return {
        name: '',
        type: 'bar',
        data: []
    }
};
var options = [];
$("#submit").click(function(){
    var jq = $("#jq").val();
    //进行ajax交互
 
   console.log(jq);
   $.LoadingOverlay("show");
    $.ajax({
        headers: { "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').val() },
        url: "/RecentState",
        type: "POST",
        data: {"jq":jq},
        success: function (res) {
            $("#resultDiv").empty();
            options = [];
            $.LoadingOverlay("hide");
           if(res.code == 0){
            $("#resultDiv").append('<div class = "row"><div class = "col-xs-3"><label for="resultSelect">请选择时间：</label>' + 
            '<select class="form-control" id="resultSelect" name="resultSelect">'

         
             + '</select></div></div>');
             var commentDiv =  
             '<div id=' + "'" + "comments" + "'" + ' style="width:100%;height:400px;float:left"/>';
             var gradeDiv = '<div id=' + "'" + "grades" + "'" + ' style="width:100%;float:left;height:400px;"/>'
             $("#resultDiv").append(commentDiv);
             $("#resultDiv").append(gradeDiv);
          var data = res.data;
          console.log(data);
          //进行图表的绘制
          for(var i = 0; i < data.times.length;i++){
              var time = data.times[i];
              var commentOption = {
                title:{
                    text: "评论变化图："
                },
                tooltip:{
                    trigger:"axis"
                },
                //折现有几条
                legend:{
                    data:[]
                },
                xAxis : 
                    {
                       
                        data : data.platforms
                    }
                ,
                yAxis : {
                    // {
                    //     type : 'value',
                    //     axisLabel : {
                    //         formatter: '{value}'
                    //     }
                    // }
                },
                series: [{
                    name: '',
                    type: 'bar',
                    data: []
                }
                ],
            };

            var gradeOption = {
                title:{
                    text:"评分变化图："
                },
                tooltip:{
                    trigger:"axis"
                },
                //折现有几条
                legend:{
                    data:[]
                },
                xAxis : 
                    {
                      
                        data : data.platforms
                    }
                ,
                yAxis : {
                    // {
                    //     type : 'value',
                    //     axisLabel : {
                    //         formatter: '{value}'
                    //     }
                    // }
                },
                series: [{
                    name: '',
                    type: 'bar',
                    data: []
                }]
            }








              for(var j = 0; j < time.platforms.length;j++){
   
                 commentOption.series[0].data.push(time.platforms[j].commentValue);
    
             gradeOption.series[0].data.push(time.platforms[j].gradeValue);
              }
              var option = {
                "time": data.times[i].time,
                options:[commentOption,gradeOption]
            };
            options.push(option);
        
            console.log(data.times[i].time);
            $("#resultSelect").append("<option value=" + "'" +data.times[i].time + "'" + ">" + data.times[i].time  + "</option>"); 
          
        }
        console.log(111);
            var commentChart = echarts.init(document.getElementById("comments"));
            console.log(222);
            console.log(options[0].options[0]);
            commentChart.setOption(options[0].options[0]);
            console.log(333);
            var gradeChart = echarts.init(document.getElementById("grades"));
            gradeChart.setOption(options[0].options[1]); 
    
            //查看平台选择变化
$("#resultSelect").change(function(){
   
    console.log(999999);
    var i = 0;
    for(;i < options.length;i++)
    if(options[i].time ==  $("#resultSelect").val())
    break;
    var commentChart = echarts.init(document.getElementById("comments"));
    commentChart.setOption(options[i].options[0], true);
    var gradeChart = echarts.init(document.getElementById("grades"));
    gradeChart.setOption(options[i].options[1], true);
})
        
           }else{
               swal("请求失败",res.message,"error");
           }

        },
        error:function (res){
            $.LoadingOverlay("hide");
            swal("请求失败","请尝试再次请求","error");
        }
})
 return false;
});
