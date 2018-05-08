  $("#tijiao").click(function () {
       var year = $("#year").val();
       var month = [];
       var jq = [];
       obj1 = document.getElementsByName("jq");
       for (k in obj1) {
           if (obj1[k].checked)
               jq.push(obj1[k].value);
       }
       obj2 = document.getElementsByName("month");
        for(k in obj2) {
            if (obj2[k].checked)
                month.push(obj2[k].value);
        }
       $.ajax({
               headers: {"X-CSRFToken": $('[name="csrfmiddlewaretoken"]').val()},
               url: "/alljq",
               type: "POST",
               data: {'jq': JSON.stringify(jq),'year':year,'month':JSON.stringify(month)},
               success: function (data) {

                   var myChartone = echarts.init(document.getElementById('main1'));
                   var Item = function () {
                       return {
                           name: '',
                           type: 'line',
                           data: []
                       }
                   };
                   var Series = [];
                    for(var i=0;i<jq.length;i++){
                        var it = new Item();
                        it.name = jq[i];
                        it.data = data[jq[i]]['month_number'];
                        Series.push(it);
                    }
                    var option1 = {
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data:jq
    },
    xAxis:  {
        type: 'category',
        boundaryGap: false,
        data: data[jq[0]]['month']
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            formatter: '{value}'
        }
    },
    series: []
};
            option1.series = Series;

                   myChartone.setOption(option1,true);
               },
                error:function () {
                    alert('error')

                }
           }
       )

       return false;
   }
   );