var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};

var option;

 myChart.showLoading();
 chrome.bookmarks.getTree((res) => {
     // var book_marks = res[0]["children"][0]["children"][2]
     var book_marks = JSON.stringify(res).replace(/title/g, "name")
     console.log(book_marks);
     // alert(book_marks)
     myChart.hideLoading();
     myChart.setOption(
         (option = {
             tooltip: {
                 trigger: 'item',
                 triggerOn: 'mousemove'
             },
             textStyle: {
               fontFamily: 'Microsoft YaHei',
               fontSize: 8,
               fontStyle: 'normal',
               fontWeight: 'normal'
             },
             series: [
                 {
                     type: 'tree',
                     data: JSON.parse(book_marks),
                     top: '18%',
                     bottom: '14%',
                     layout: 'radial',
                     symbol: 'emptyCircle',
                     symbolSize: 7,
                     initialTreeDepth: 4,
                     animationDurationUpdate: 750,
                     emphasis: {
                         focus: 'descendant'
                     }
                 }
             ]
         })
     );

 });


if (option && typeof option === 'object') {
    myChart.setOption(option);
}

$(window).on('resize', function () {
    if (myChart != null && myChart != undefined) {
        myChart.resize();
    }
});

myChart.on('click', function (params) {
    if (params.data && params.data.url) {
        window.open(params.data.url);
    }
});