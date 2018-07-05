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
  
    var years = [];
    var platforms = [];
    var startDate = $("#startDate").val();
    var endDate =  $("#endDate").val();
    var time = $("#time").val(); 
   years = $("#year").val();
   platforms = $("#platform").val();
   //查看是否有所有标签被选上

  
    var errMes = "";
    if(years.length == 0)
    errMes += "未选择比较年份，"
    if(platforms.length == 0)
      errMes += "未选择平台，";
    
      if(startDate > endDate)
      errMes += "开始时间不能大于结束时间"
    if(errMes != "")
    swal("提醒",errMes,"warning");  
     else{
        $.LoadingOverlay("show"); 
    var param = {
        'platforms':JSON.stringify(platforms),
        'startDate':startDate,
        'endDate':endDate,
        'years':JSON.stringify(years),
        'time':time
    };
    console.log(param);
    $.ajax({
            headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
            url:"/ComparedAnalysis",
            type:"POST",
            data:param,
            success:function (res) {
                console.log(res);
                $.LoadingOverlay("hide"); 
                options = [];
                $("#resultDiv").empty();
                    $.LoadingOverlay("hide");
                    if(res.code == 0){
                        $("#resultDiv").empty();
                        $("#resultDiv").append('<div class = "row"><div class = "col-xs-3"><label for="resultSelect">请选择平台：</label>' + 
                        '<select class="form-control" id="resultSelect" name="resultSelect">'
            
                     
                         + '</select></div></div>');
                         var commentDiv =  
                         '<div id=' + "'" + "comments" + "'" + ' style="width:100%;height:400px;float:left"/>';
                         var gradeDiv = '<div id=' + "'" + "grades" + "'" + ' style="width:100%;float:left;height:400px;"/>'
                         $("#resultDiv").append(commentDiv);
                         $("#resultDiv").append(gradeDiv);
                    var data = res.data;
                    console.log(data);
                    for(var i = 0; i < data.platforms.length;i++){
        
                    var commentOption = {
                        title:{
                            text:"评论数量变化图：\n"
                        },
                        tooltip:{
                            trigger:"axis"
                        },
                        //折现有几条
                        legend:{
                            data:[' ']
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
                            data:[' ']
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
        
        
        
                        for(var j = 0; j < data.platforms[i].years.length;j++){
                            var year =  data.platforms[i].years[j];
                            commentOption.legend.data.push(year.year);
                            gradeOption.legend.data.push(year.year);
                                var commentItem = new Item();
                                commentItem.name = year.year;
                                commentItem.data = year.commentValue;
                                commentOption.series.push(commentItem);
                                var gradeItem = new Item();
                                gradeItem.name = year.year;
                                gradeItem.data = year.gradeValue;
                                gradeOption.series.push(gradeItem);
                            
                        }
                       
          
                        var option = {
                            "platformName": data.platforms[i].platform,
                            options:[commentOption,gradeOption]
                        };
                        options.push(option);
               
                      console.log(111);
                      console.log(data.platforms[i].platform);
                      $("#resultSelect").append("<option value=" + "'" + data.platforms[i].platform + "'" + ">" + data.platforms[i].platform + "</option>"); 
                    
                    }
                    console.log(222);
                    console.log(options[0].platformName);
                     var commentChart = echarts.init(document.getElementById("comments"));
                         commentChart.setOption(options[0].options[0], true);
                         var gradeChart = echarts.init(document.getElementById("grades"));
                         gradeChart.setOption(options[0].options[1], true);
    //查看景区选择变化
$("#resultSelect").change(function(){
   
    console.log(999999);
    var i = 0;
    for(;i < options.length;i++)
    if(options[i].platformName ==  $("#resultSelect").val())
    break;
    var commentChart = echarts.init(document.getElementById("comments"));
    commentChart.setOption(options[i].options[0], true);
    var gradeChart = echarts.init(document.getElementById("grades"));
    gradeChart.setOption(options[i].options[1], true);
})
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