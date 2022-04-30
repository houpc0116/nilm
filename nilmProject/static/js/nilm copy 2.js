//隨機產生十六進位color
function randomColor(){ 
  var colorStr=Math.floor(Math.random()*0xFFFFFF).toString(16).toUpperCase(); 
  return"#"+"000000".substring(0,6-colorStr)+colorStr;
}

//顯示目前時間
function getCurrentTime(){
  var now=new Date();//生成日期物件(完整的日期資訊)
  var y=now.getFullYear();//年份
  var M=now.getMonth()+1>9?now.getMonth()+1:'0'+(now.getMonth()+1); //月份
  var d=now.getDate()>9?now.getDate():'0'+now.getDate();//日期
  var h=now.getHours()>9?now.getHours():'0'+now.getHours();//小時
  var m=now.getMinutes()>9?now.getMinutes():'0'+now.getMinutes();//分鐘
  var currentdate = y+'-'+M;
  //var currentdate = y+'-'+M+'-'+d+' '+h+':'+m;
  return currentdate;
}

//date为传入日期
function getDuration (date) {    
  // how many days of this month   
  let dt = new Date(date)    
  var month = dt.getMonth()    
  dt.setMonth(dt.getMonth() + 1)   
  dt.setDate(0);  
  return dt.getDate()  
}

function initChartPromse(device){
   return new Promise(function(resolve, reject) {
      setTimeout(function() {
          let domain = window.location.hostname;
          let port = window.location.port;
          let url = 'http://'+domain+':'+port+'/api/sensor/?device='+device;
          $.ajax({
            //url: '/api/sensor/?device='+device,
            url: url,
            type: "GET",
            cache: false,
            async: false,
            data: {
              myData: "Here's my posted data!"
            },
            beforeSend: function (xhr) {
              //$('.loading').html("<img src='{% static 'img/preloader.gif' %}' with='100' height='100'>");//Loading
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (obj) {
              //console.log(obj);
              let Obj = obj.sort(function (a, b) { return a.datetime > b.datetime ? 1 : -1; });  //排序 ASC
              //console.log(Obj.length);
              $('.dateTime').text(Obj[Obj.length -1]['datetime']);  //更新時間
              $('.vo').text(Obj[Obj.length -1]['vo']);  //電壓
              $('.cu').text(Obj[Obj.length -1]['cu']);  //電流
              $('.activeVal').text(Obj[Obj.length -1]['active']);  //有效功率
              $('.reactive').text(Obj[Obj.length -1]['reactive']);  //無效功率
              $('.apparent').text(Obj[Obj.length -1]['apparent']);  //視在功率
              $('.pf').text(Obj[Obj.length -1]['pf']);  //功率因數
              $('.freq').text(Obj[Obj.length -1]['freq']);  //頻率
              //直線圖
              $.each(Obj, function(key, val){
                  //最多顯示點數
                  if(yAxis.length>arrayrang){
                      yAxis.shift();
                  }
                 /* if(yTime.length>arrayrang){
                      yTime.shift();
                  } */
                  if(datas1.length>arrayrang){
                      datas1.shift();
                  }
                 /* if(datas2.length>arrayrang){
                      datas2.shift();
                  } */
                  //console.log(val.datetime);
                  yAxis.push(val.datetime);
                  datas1.push( parseFloat(val.active) );
                  //datas2.push( parseFloat(val.cu) );
              });
              //直線圖
              for(var i=1; i<= mondays; i++){
                 if(i<10){ i = "0"+i}  //日期

                 let showdate = ndate+"-"+i;
                 newArrDate.push(showdate); //儲存日期
                 
                 //找出相對應日期的資料
                 var findObj = Obj.filter(function(item, index, array){
                     if(item.datetime.indexOf(showdate) != -1)
                        return item;
                 });
                 //console.log(findObj);
                 //findObj = findObj.sort(function (a, b) { return a.datetime < b.datetime ? 1 : -1; });  //排序 DESC
                 //console.log(findObj[0]);
                 if(findObj.length != 0){
                    let kw = 0;
                    findObj.forEach(function(item, index, array){
                        kw += item['active'];
                    });
                    newArrCount.push(parseFloat(kw));
                 }else{
                    newArrCount.push(0);
                 }
              }

            },
            error: function (error) {
              console.log(error);
            }
          });
          resolve('ok');
      }, 100);
   });

}



function initReddChartPromse(house){
  return new Promise(function(resolve, reject) {
    setTimeout(function() {
      let domain = window.location.hostname;
      let port = window.location.port;
      //let url = '/redd/get/dataset'+house+'/';
      //let url = '/reddataset/?houseId='+house;
      let url = 'http://'+domain+':'+port+'/reddataset/houseId'+house+'/';
      $.ajax({
        //url: '/redd/get/dataset'+house+'/',
        url: url,
        type: "GET",
        cache: false,
        async: false,
        data: {
          myData: "Here's my posted data!"
        },
        beforeSend: function (xhr) {
          //$('.loading').html("<img src='{% static 'img/preloader.gif' %}' with='100' height='100'>");//Loading
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (obj) {
          //console.log(obj['data1']);
          let Obj = obj['data'].sort(function (a, b) { return a.datetime > b.datetime ? 1 : -1; });  //排序 ASC
          //console.log(Obj);
          //Line
          $.each(Obj, function(key, val){
            //console.log(val);
            if(val.device == 'mains_1'){
              yAxis.push( val.datetime );
              datas1.push( val.pw );
            }else{
              datas2.push( val.pw );
            }
          });
          //Pie
          //console.log(obj['data1']);
          let getColor = '';
          $.each(obj['data1'], function(key, val){
             dataTime.push(val.datetime);
             labels.push(val.device);
             datas3.push(val.pw);
             getColor = randomColor();
             color.push(getColor);
             //console.log(getColor);
             str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>'+val.device;
          });
          //console.log(randomColor());
        },
        error: function (error) {
          console.log(error);
        }
      });
      resolve('ok');
    }, 100);
  });
}

function initUKChartPromse(house){
  return new Promise(function(resolve, reject) {
    setTimeout(function() {
      let domain = window.location.hostname;
      let port = window.location.port;
      //let url = 'http://'+domain+':'+port+'/ukdale/get/dataset'+house+'/';
      let url = 'http://'+domain+':'+port+'/ukdataset/houseId'+house+'/';
      $.ajax({
        //url: '/ukdale/get/dataset'+house+'/',
        url: url,
        type: "POST",
        cache: false,
        async: false,
        data: {
          myData: "Here's my posted data!"
        },
        beforeSend: function (xhr) {
          //$('.loading').html("<img src='{% static 'img/preloader.gif' %}' with='100' height='100'>");//Loading
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (obj) {
          //console.log(obj['data1']);
          let Obj = obj['data'].sort(function (a, b) { return a.datetime > b.datetime ? 1 : -1; });  //排序 ASC
          //console.log(Obj);
          //Line
          $.each(Obj, function(key, val){
            //console.log(val);
            //if(val.device == 'AGGREGATE_1'){
              yAxis.push( val.datetime );
              datas1.push( val.pw );
            //}
          });
          //Pie
          let getColor = '';
          $.each(obj['data1'], function(key, val){
             dataTime.push(val.datetime);
             labels.push(val.device);
             datas3.push(val.pw);
             getColor = randomColor();
             color.push(getColor);
             str += '<div><i class="fas fa-circle" style="color:'+getColor+'"></i>'+val.device+'</div>';
          });
          //console.log(randomColor());
        },
        error: function (error) {
          console.log(error);
        }
      });
      resolve('ok');
    }, 100);
  });
}



//開啟連線
function open(e){
   console.log('Connection');
}


//失敗
function fail(e){
  //console.log('error');
  if (e.readyState == EventSource.CLOSED) {
    // 連線已關閉
    console.log('close');
    evtSource.close();
  }
}

//接收訊息
function noticeContent(e){
  let obj = JSON.parse(e.data);
  //console.log(devItem[0]['id']);
  if(devItem[0]['id'] == obj['device']){
    $('.dateTime').text(obj['datetime']);  //更新時間
    $('.vo').text(obj['vo']);  //電壓
    $('.cu').text(obj['cu']);  //電流
    $('.activeVal').text(obj['active']);  //有效功率
    $('.reactive').text(obj['reactive']);  //無效功率
    $('.apparent').text(obj['apparent']);  //視在功率
    $('.pf').text(obj['pf']);  //功率因數
    $('.freq').text(obj['freq']);  //頻率
  
    let count =yAxis.length;
    let date_time = obj['datetime'].replace(' ', 'T');
    
    if( yAxis[count -1] != date_time && yAxis.length != 0 ){
      //折線圖
      //console.log(yAxis[count-1]);
      if(yAxis.length>arrayrang){
        yAxis.shift();
      }

      if(datas1.length>arrayrang){
        datas1.shift();
      }
      yAxis.push(date_time);
      datas1.push( parseFloat(obj['active']) );
      myLineChart.update();   //更新圖表
      //直線圖
      let nowdate = ndate+"-"+today;
      let findKey = findIndexPos(newArrDate, nowdate);  //返回值為Key值, 沒有找到為-1
      if(findKey != -1){
        //console.log(typeof obj['active']);  
        let total = parseFloat(myChartBar.data.datasets[0].data[findKey] + obj['active']);
        myChartBar.data.datasets[0].data[findKey] = total;
        myChartBar.update();
        //console.log(newArrCount);
      }
    }

  }
}


//URL 解析
function getQueryVariableVal(param, variable) {
  var query = param.substring(0);
  var vars = query.split('&');
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split('=');
    if (decodeURIComponent(pair[0]) == variable) {
      return decodeURIComponent(pair[1]);
    }
  }
  console.log('Query variable %s not found', variable);
}


//取出今日的日期
function getCurrentDate(){
  var now=new Date();//生成日期物件(完整的日期資訊)
  var d=now.getDate()>9?now.getDate():'0'+now.getDate();//日期

  return d;
}

//找尋位置
function findIndexPos(arrayObj, id){ 
  return arrayObj.indexOf(id);
}