
//应该通过与ajax交互
$("#submit").click(function(){
 //获取各个时间节点
 var name = $("#name").val();
 var year = $("#year").val();
 var month = $("#month").val();
 var time = $("input[name='time']:checked").val();
//进行ajax交互
var param = {
  name:$("#name").val(),
   year:$("#year").val(),
   month:$("#month").val(),
   time:$("input[name='time']:checked").val()
};

  $.ajax({
  headers: {"X-CSRFToken": $('[name="csrfmiddlewaretoken"]').val()},
  url: "/singlejq",
  type: "POST",
  data:{"param":JSON.stringify(param)},
 success:function(data){
 console.log(data);
  if(data.success){
 var message = data.message;
 var tbody = "";
 //首先message元素的所有子元素
 $("#meassage").empty();
$.each(message,function(key,value){
//景区信息
var trs = "";
trs += " <p> " + key +" </p> <p>" + value +"</p>";
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
                 data:[]
             },
             xAxis: {
                 data: data.list1
             },
             yAxis: {},
             series: [{
                 name: '',
                 type: 'bar',
                 data: data.list2
             }]
         };
         var option1 = {
     tooltip: {
         trigger: 'axis'
     },
     legend: {
         data:['差评数','中评数','好评数']
     },
     xAxis:  {
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
             name:'差评数',
             type:'line',
             data:data.chaping
         },
         {
             name:'中评数',
             type:'line',
             data:data.zhongping
         },
          {
             name:'好评数',
             type:'line',
             data:data.haoping
         }
     ]
 };
         myChart.setOption(option);
         myChartone.setOption(option1);
 }else{
 swal("请求失败","请查看景区名字是否合法","warning");
 }
 },
  error:function (error) {
  console.log(error);
                   swal("请求失败","请尝试再次刷新","error");

                }


})
return false;








});
