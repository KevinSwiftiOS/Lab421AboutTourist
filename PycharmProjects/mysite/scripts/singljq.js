

doucumet.
        var colors = ['#5793f3', '#d14a61', '#675bba'];
        var myChart = echarts.init(document.getElementById('main'));
        var myChartone = echarts.init(document.getElementById('main1'));
        var option = {
            tooltip: {},
            legend: {
                data:[]
            },
            xAxis: {
                data: {{list1|safe}}
            },
            yAxis: {},
            series: [{
                name: '',
                type: 'bar',
                data: {{list2|safe}}
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
        data: {{ list3|safe }}
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
            data:{{ list4|safe }},
        },
        {
            name:'中评数',
            type:'line',
            data:{{ list5|safe }},
        },
         {
            name:'好评数',
            type:'line',
            data:{{ list6|safe }},
        }
    ]
};
        myChart.setOption(option);
        myChartone.setOption(option1);