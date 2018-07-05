
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
var options = [];
//根据时间间隔动态选择option的值
$("#time").change(function(){
    var  time = $("#time").val();
    $("#startDate").empty();
    $("#endDate").empty();
    $("#startDateDiv").empty();
    $("#endDateDiv").empty();
   switch (time){
     
       case "season":
       $("#startDateDiv").append('<label for="startDate" id = "startDateText">请选择开始季度：</label>' + 
       '<select class="form-control" id="startDate" name="startDate">'
    
        + '</select>');
        $("#endDateDiv").append('<label for="endDate" id = "endDateText">请选择结束季度：</label>' + 
        '<select class="form-control" id="endDate" name="endDate">'
     
         + '</select>');
       for(var i = 1; i <= 4;i++) {
      $("#startDate").append("<option value=" + "'" + i + "'" + ">" + i + "</option>"); 
       $("#endDate").append("<option value=" + "'" + i + "'" + ">" + i + "</option>"); 
       }
       break;
       case "month":
     $("#startDateDiv").append('<label for="startDate" id = "startDateText">请选择开始月份：</label>' + 
        '<select class="form-control" id="startDate" name="startDate">'
     
         + '</select>');
         $("#endDateDiv").append('<label for="endDate" id = "endDateText">请选择结束月份：</label>' + 
         '<select class="form-control" id="endDate" name="endDate">'
      
          + '</select>');  
       for(var i = 1; i <= 12;i++) {
       $("#startDate").append("<option value=" + "'" + i + "'" + ">" + i + "</option>"); 
       $("#endDate").append("<option value=" + "'" + i + "'" + ">" + i + "</option>"); 
       }
       break;
       case "week":
       $("#startDateDiv").append('<label for="startDate" id = "startDateText">请选择开始周：</label>' + 
       '<select class="form-control" id="startDate" name="startDate">'
    
        + '</select>');
        $("#endDateDiv").append('<label for="endDate" id = "endDateText">请选择结束周：</label>' + 
        '<select class="form-control" id="endDate" name="endDate">'
     
         + '</select>');
       for(var i = 1; i <= 52;i++) {
       $("#startDate").append("<option value=" + "'" + i + "'" + ">" + i + "</option>"); 
       $("#endDate").append("<option value=" + "'" + i + "'" + ">" + i + "</option>"); 
       }
       break;
       default:
       break;

   }
})



$("#submit").click(function () {
     
 
    var jqs = [];
    var  platforms = [];
    //开始与结束月份获取
    var startYear = $("#startYear").val();   
    var startDate = $("#startDate").val();   
    var endYear = $("#endYear").val();   
    var endDate = $("#endDate").val();   
    var  time = $("#time").val();
    //景区获取
 jqs = $("#jq").val();
 platforms = $("#platform").val();
   //查看是否有所有标签被选上
   //是否是所有景区的
  

  
    var errMes = "";
    if(jqs.length == 0)
    errMes += "未选择景区，"
    if(platforms.length == 0)
      errMes += "未选择平台，";
      if(startYear > endYear)
      errMes += "开始时间不能大于结束时间";
      if(startYear == endYear && startDate > endDate)
      errMes += "开始时间不能大于结束时间"
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
        'time':time,
       
    };
 
    $.ajax({
        headers: { "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').val() },
        url: "/InnerScenic",
        type: "POST",
        data: param,
        success: function (res) {
            
            $.LoadingOverlay("hide");
            $("#resultDiv").empty();
            options = [];
            if(res.code == 0){
            var data = res.data;
        
         
         
            $("#resultDiv").append('<div class = "row"><div class = "col-xs-3"><label for="resultSelect">请选择景区：</label>' + 
            '<select class="form-control" id="resultSelect" name="resultSelect">'

         
             + '</select></div></div>');
             var commentDiv =  
             '<div id=' + "'" + "comments" + "'" + ' style="width:100%;height:400px;float:left"/>';
             var gradeDiv = '<div id=' + "'" + "grades" + "'" + ' style="width:100%;float:left;height:400px;"/>'
             $("#resultDiv").append(commentDiv);
             $("#resultDiv").append(gradeDiv);
            for(var i = 0; i < data.jqs.length;i++){

            var commentOption = {
                title:{
                    text:"评论变化图："
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
                    text:"评分变化图："
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
               
                var option = {
                    "jqName": data.jqs[i].jq,
                    options:[commentOption,gradeOption]
                };
                options.push(option);
       
           
              $("#resultSelect").append("<option value=" + "'" + data.jqs[i].jq + "'" + ">" + data.jqs[i].jq  + "</option>"); 
            
            }
   
             var commentChart = echarts.init(document.getElementById("comments"));
                 commentChart.setOption(options[0].options[0], true);
                 var gradeChart = echarts.init(document.getElementById("grades"));
                 gradeChart.setOption(options[0].options[1], true);
//查看景区选择变化
$("#resultSelect").change(function(){
   
 
    var i = 0;
    for(;i < options.length;i++)
    if(options[i].jqName ==  $("#resultSelect").val())
    break;
    var commentChart = echarts.init(document.getElementById("comments"));
    commentChart.setOption(options[i].options[0], true);
    var gradeChart = echarts.init(document.getElementById("grades"));
    gradeChart.setOption(options[i].options[1], true);
})
            }




    










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
