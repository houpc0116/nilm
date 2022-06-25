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

//顯示目前時間
function getCurrentTime1(){
  var now=new Date();//生成日期物件(完整的日期資訊)
  var y=now.getFullYear();//年份
  var M=now.getMonth()+1>9?now.getMonth()+1:'0'+(now.getMonth()+1); //月份
  var d=now.getDate()>9?now.getDate():'0'+now.getDate();//日期
  var h=now.getHours()>9?now.getHours():'0'+now.getHours();//小時
  var m=now.getMinutes()>9?now.getMinutes():'0'+now.getMinutes();//分鐘
  var s=now.getSeconds()>9?now.getSeconds():'0'+now.getSeconds();//秒
  var currentdate = '';
  currentdate = y+'-'+M+'-'+d+'T'+h+':'+m+':'+s;
  
  return currentdate;
}

//顯示目前日期
function getCurrentToday(){
  var now=new Date();//生成日期物件(完整的日期資訊)
  var y=now.getFullYear();//年份
  var M=now.getMonth()+1>9?now.getMonth()+1:'0'+(now.getMonth()+1); //月份
  var d=now.getDate()>9?now.getDate():'0'+now.getDate();//日期
  var h=now.getHours();//小時
  //var m=now.getMinutes()>9?now.getMinutes():'0'+now.getMinutes();//分鐘
  //var s=now.getSeconds()>9?now.getSeconds():'0'+now.getSeconds();//秒
  var currentdate = '';
  currentdate = y+'-'+M+'-'+d;
  
  var obj = {'today':currentdate, 'hours':h};
  return obj;
}


function initChartPromse(device){
  return new Promise(function(resolve, reject) {
    setTimeout(function() {
        let domain = window.location.hostname;
        let port = window.location.port;
        let url = 'http://'+domain+':'+port+'/statistic/?device='+device;
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
              //顯示月份統計
                //console.log(obj);
                //console.log(obj['week_date']); 
                let Obj = obj['data'].sort(function (a, b) { return a.datetime > b.datetime ? 1 : -1; });  //排序 ASC
                //console.log(Obj); 
                //直線圖
                let todayObj = getCurrentToday();
                //console.log(todayObj['hours']);
                for(let i=0; i<=todayObj['hours']; i++){
                    //console.log(i);
                    let h = i<=9?'0'+i:i;
                    newArrDate.push(h);

                    let filterDate = todayObj['today']+' '+h;
                    //console.log(filterDate);
                    var findObj = obj['data'].filter(function(item, index, array){
                        if((item.datetime).indexOf(filterDate) != -1)
                            return item;
                    });
                    //console.log(findObj);
                    let kw = 0;
                    findObj.forEach(function(item, index, array){
                        kw += item['active'];
                    });
                    newArrCount.push(kw);
                }
                //Pie
/*
                $.each(obj['data'], function(key, val){
                  if(device == 'elec110'){
                      if(labels.indexOf(machine) == -1 && val.device != 'elec110') {
                          if(val.device == 'plug1-1'){
                            labels.push('筆記型電腦');
                          }else if(val.device == 'plug1-2'){
                            labels.push('空氣清淨機');
                          }
                         //labels.push(machine);
                         //顏色
                         getColor = randomColor();
                         color.push(getColor);
                         str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>'+machine;
                      }
                  }
                });
*/
                //筆記型電腦
                let total = 0;
                var findObj = obj['data'].filter(function(item, index, array){
                        if(item.device == 'plug1-1')
                          return item;
                  });
                for(let i=0; i<findObj.length; i++){
                  total += findObj[i]['active'];
                }
                labels.push('筆記型電腦');
                datas4.push(total);
                //顏色
                getColor = "#4e73df";
                color.push(getColor);
                str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>筆記型電腦';
                //空氣清淨機
                let total1 = 0;
                var findObj = obj['data'].filter(function(item, index, array){
                        if(item.device == 'plug1-2')
                          return item;
                  });
                for(let i=0; i<findObj.length; i++){
                  total1 += findObj[i]['active'];
                }
                labels.push('空氣清淨機');
                datas4.push(total1);
                //顏色
                getColor = "#1cc88a";
                color.push(getColor);
                str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>空氣清淨機';
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
          //let getColor = '';
          color =['#4e73df','#1cc88a','#36b9cc'];
          let i =0;
          $.each(obj['data1'], function(key, val){
            dataTime.push(val.datetime);
            labels.push(val.device);
            datas3.push(val.pw);
             
            str += '<i class="fas fa-circle" style="color:'+color[i]+'"></i>'+val.device;

            i+=1;
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
          //let getColor = '';
          //console.log(obj['data1']);
          //let getColor = '';
          let total = 0;
/*
          $.each(obj['data1'], function(key, val){
            if(labels.indexOf(val.device) == -1 ) {
              labels.push(val.device);
              //顏色
              getColor = randomColor();
              color.push(getColor);
              str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>'+val.device;
            }
          });
*/          
          //洗衣機
          var findObj = obj['data1'].filter(function(item, index, array){
                if(item.device == 'washing_machine_5')
                  return item;
              });
          for(let i=0; i<findObj.length; i++){
              total += findObj[i]['pw'];
          }
          labels.push('洗衣機');
          datas3.push(total);
          //顏色
          getColor = "#4e73df";
          color.push(getColor);
          str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>洗衣機';
          //水壶
          var findObj = obj['data1'].filter(function(item, index, array){
                if(item.device == 'kettle_10')
                  return item;
              });
          for(let i=0; i<findObj.length; i++){
              total += findObj[i]['pw'];
          }
          labels.push('燙斗');
          datas3.push(total);
          //顏色
          getColor = "#1cc88a";
          color.push(getColor);
          str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>燙斗';
          //微波爐
          var findObj = obj['data1'].filter(function(item, index, array){
                  if(item.device == 'microwave_13')
                    return item;
              });
          for(let i=0; i<findObj.length; i++){
              total += findObj[i]['pw'];
          }
          labels.push('冰箱');
          datas3.push(total);
          //顏色
          getColor = "#36b9cc";
          color.push(getColor);
          str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>冰箱';
          /*
          $.each(obj['data1'], function(key, val){
             dataTime.push(val.datetime);
             labels.push(val.device);
             datas3.push(val.pw);
             getColor = randomColor();
             color.push(getColor);
             str += '<div><i class="fas fa-circle" style="color:'+getColor+'"></i>'+val.device+'</div>';
          }); */ 
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

function initiAWEChartPromse(){
   return new Promise(function(resolve, reject) {
      setTimeout(function() {
          let domain = window.location.hostname;
          let port = window.location.port;
          //let url = 'http://'+domain+':'+port+'/iawedataset/?device='+device;
          let url = 'http://'+domain+':'+port+'/iawedataset/';
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
              console.log(obj);
              
              let Obj = obj['data'].sort(function (a, b) { return a.datetime > b.datetime ? 1 : -1; });  //排序 ASC
              //Line
              $.each(Obj, function(key, val){
                //console.log(val);
                if(val.device == 'mains_1'){
                  yAxis.push( val.datetime );
                  datas1.push( val.active );
                }else{
                  datas2.push( val.active );
                }
              });
              //Pie
              let getColor = '';
              let total = 0;
            /*  $.each(obj['data1'], function(key, val){
                  if(labels.indexOf(val.device) == -1 ) {
                    labels.push(val.device);
                    //顏色
                    getColor = randomColor();
                    color.push(getColor);
                    str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>'+val.device;
                  }
              });
              */
              //洗衣機
              var findObj = obj['data1'].filter(function(item, index, array){
                        if(item.device == 'washing_6')
                          return item;
                  });
              for(let i=0; i<findObj.length; i++){
                  total += findObj[i]['active'];
              }
              labels.push('洗衣機');
              datas3.push(total);
              //顏色
              getColor = "#4e73df";
              color.push(getColor);
              str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>洗衣機';
              //燙斗
              var findObj = obj['data1'].filter(function(item, index, array){
                        if(item.device == 'iron_8')
                          return item;
                  });
              for(let i=0; i<findObj.length; i++){
                  total += findObj[i]['active'];
              }
              labels.push('燙斗');
              datas3.push(total);
              //顏色
              getColor = "#1cc88a";
              color.push(getColor);
              str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>燙斗';
              //冰箱
              var findObj = obj['data1'].filter(function(item, index, array){
                        if(item.device == 'fridge_3')
                          return item;
                  });
              for(let i=0; i<findObj.length; i++){
                  total += findObj[i]['active'];
              }
              labels.push('冰箱');
              datas3.push(total);
              //顏色
              getColor = "#36b9cc";
              color.push(getColor);
              str += '<i class="fas fa-circle" style="color:'+getColor+'"></i>冰箱';
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

//顯示電器
function showAppliancesList(){
   let dataset = $('#dataset').val();
   //alert(dataset);
   if(dataset == 'redd'){
     $('#appliances').html('');
     //<option>--請選擇電器--</option>
     $('#appliances').append("<option>--請選擇電器--</option>");
     $('#appliances').append("<option value='fridge'>冰箱</option>");
     $('#appliances').append("<option value='microwave'>微波爐</option>");
     $('#appliances').append("<option value='sockets'>插座</option>");

  }else if(dataset == 'ukdale'){
    $('#appliances').html('');
    $('#appliances').append("<option>--請選擇電器--</option>");
    $('#appliances').append("<option value='kettle'>水壺</option>");
    $('#appliances').append("<option value='microwave'>微波爐</option>");
    $('#appliances').append("<option value='wash_dryer'>洗衣機</option>");

  }else if(dataset == 'iawe'){
    $('#appliances').html('');
    $('#appliances').append("<option>--請選擇電器--</option>");
    $('#appliances').append("<option value='clothes_iron'>熨斗</option>");
    $('#appliances').append("<option value='fridge'>冰箱</option>");
    $('#appliances').append("<option value='wash_dryer'>洗衣機</option>");

  }
}

//查詢analyze
function sendFrom(){
  let dataset = $('#dataset').val();
  let algorithm = $('#algorithm').val();
  let appliances = $('#appliances').val();
  //console.log(dataset);
  if(dataset == '--請選擇資料集--'){
     alert(dataset);
  }else if(algorithm == '--請選擇演算法--'){
     alert(algorithm);
  }else if(appliances == '--請選擇電器--'){
     alert(appliances);
  }
  //預測和執行結果
  $('#resultimg').attr('src','');
  $('#resultmsg').hide();
  $.ajax({
     url:  "/predict/",  //路徑
     type: "POST",               //傳值方式
     data: "dataset="+dataset+"&algorithm="+algorithm+"&appliances="+appliances, //傳送使用者帳號
     cache: false,               //清除cache
     //失敗時處理的事件
     error: function(xhr) {
       console.log('Ajax request 發生錯誤');
     },
     //載入
     beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        $('#loading').show();
     },
     //成功傳回來的值
     success: function(response){
        data = JSON.parse(response);
        console.log(data);
        $('#loading').hide();
        $('#resultmsg').show();
        if(data['status'] != 'ok'){
           $('#resultmsg').text('Error');
        }else{
           //顯示圖片
           let domain = window.location.hostname;
           let port = window.location.port;
           let urlImg = 'http://'+domain+':'+port+'/static/analyze/'+data['image']+'.png';
           $('#resultimg').attr('src',''+urlImg+'');
           //性能指標
           let value = data['content'].split(":");
           $('#dataTable').show();
           $('.rel').text(value[0]);
           $('.mean').text(value[1]);
           //var el = document.getElementById("resultmsg");
           //el.innerHTML = data['accuracy']+'<br>'+data['precision']+'<br>'+data['recall']+'<br>'+data['f1score']+'<br>'+data['relativerror']+'<br>'+data['meanabsoluterror'];
           //$('#resultmsg').html(data['accuracy']+data['precision']+data['recall']);
        }
     },
  });
 
}