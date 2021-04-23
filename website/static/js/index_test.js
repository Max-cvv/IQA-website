$(function(){

var img_num = 2;
var col_num = 2;

leadingViewer = null;
var IS_sync = false;
var flag = 0;
var op1 = 0, op2 = 0;
var check_left = false;
var check_right = false;
var D_1,D_2,CO_1,CO_2;
var pho;
var date1,date2;

var img_count = 1;
var img_num_all = parseInt(img_num1);
var navHeight = 61;


var root_prefixUrl = static_root + "files/images/";
var rootpath = static_root + "files/photo/";

//调整图片大小位置
$("#row1").height(($("#row1").width()-col_num*30)/((4*col_num)/3));
padding_main = ((window.innerHeight - navHeight)/2 + navHeight) - $("#row1").height()/2;
$(".main").css("padding-top", padding_main);


$("#my-checkbox").bootstrapSwitch(
    {
        "size":"mini",
        "labelText":'同步',
    }
);
$("#my-checkbox").on('switchChange.bootstrapSwitch', function(event, state){
    sync_tab(); 
});



var tileSources = new Array();
var viewers = new Array();
var option = {
    id:  "img1",
    prefixUrl: root_prefixUrl,
    debugMode: false, //开启调试模式
    //debugGridColor:'#1B9E77', //调试模式下网格的颜色
    minZoomLevel: 0.5,  //最小允许放大倍数
    showNavigator:false,
    navigatorOpacity:1,
    minPixelRatio:0.5,
    minZoomImageRatio:0,
    //controlsFadeDelay:100,
    //controlsFadeLength:0,
    showZoomControl:false,
    showFullPageControl:false,
    showHomeControl:false,
    gestureSettingsMouse:{clickToZoom:false},
}

for(i = 0;i<img_num;i++){
    tileSources[i] = new OpenSeadragon.TileSource;
    tileSources[i] = {
        Image: 
        {
            xmlns:  "http://schemas.microsoft.com/deepzoom/2009",
            Url: "",
            Overlap: "1",
            TileSize: "256",
            Format : "jpg",
            Size:
            {
                Height: "",
                Width:  "",
            }
        }
    }
    imgid = i+1;
    option.id = "img"+imgid;
    viewers[i] = OpenSeadragon(option);
}


get_next()

var op_log1 = function(){
    op1 = op1 + 1;
}

var op_log2 = function(){
    op2 = op2 + 1;
}


viewers[0].addHandler( 'canvas-drag-end', op_log1);
viewers[1].addHandler( 'canvas-scroll', op_log2);

viewers[0].addHandler( 'canvas-drag-end', op_log1);
viewers[1].addHandler( 'canvas-scroll', op_log2);

viewers[0].addHandler( 'canvas-click', ck_left);
viewers[1].addHandler( 'canvas-click', ck_right);

sync_tab(); 

$(document).keyup(function(event){
    if(event.keyCode ==13){
      $("#start-btn").trigger("click");
    }
});

$("#reset-img").click(function(){
    //alert("窗口:"+window.innerWidth+"屏幕:"+ screen.width);
    viewers[0].viewport.goHome();
    viewers[1].viewport.goHome();
});

$("#reset-choice").click(function(){
    check_right = false;
    check_left = false;
    $('#label_left').removeClass("labelActive");
    $('.openseadragon-container:first').removeClass("imgchosen");
    $('#label_right').removeClass("labelActive");
    $('.openseadragon-container:last').removeClass("imgchosen");
});


$("#start-btn").click(function(){

    $(".progress-bar").css('width', (img_count/img_num_all)*100+'%');
    if(img_count == img_num_all-1){
        $("#start-btn").html("提交");
    }
    if(img_count<img_num_all){
        img_count++;
        if(check_right || check_left)
        {
            var record_ajax = get_records();
            $.when(record_ajax).done(function () {
                get_next();
            });
            $('#label_right').removeClass("labelActive");
            $('.openseadragon-container:last').removeClass("imgchosen");
            $('#label_left').removeClass("labelActive");
            $('.openseadragon-container:first').removeClass("imgchosen");
            check_right = false;
            check_left = false;
        }
        else{
            get_next();
        }
    }
    else{
        submit();
    }

    
})


function ck_left(){
    if(!check_left&&!check_right){
        $('#label_left').addClass("labelActive");
        $('.openseadragon-container:first').addClass("imgchosen");
        check_left = true;
    }
    else if(check_left){
        //$('#label_left').removeClass("labelActive");
        //$('.openseadragon-container:first').removeClass("imgchosen");
        //check_left = false;
    }
    else{
        $('#label_left').addClass("labelActive");
        $('.openseadragon-container:first').addClass("imgchosen");
        $('#label_right').removeClass("labelActive");
        $('.openseadragon-container:last').removeClass("imgchosen");
        check_left = true;
        check_right = false;
    }
}

function ck_right(){
    if(!check_left&&!check_right){
        $('#label_right').addClass("labelActive");
        $('.openseadragon-container:last').addClass("imgchosen");
        check_right = true;
    }
    else if(check_right){
        //$('#label_right').removeClass("labelActive");
        //$('.openseadragon-container:last').removeClass("imgchosen");
        //check_right = false;
    }
    else{
        $('#label_right').addClass("labelActive");
        $('.openseadragon-container:last').addClass("imgchosen");
        $('#label_left').removeClass("labelActive");
        $('.openseadragon-container:first').removeClass("imgchosen");
        check_right = true;
        check_left = false;
    }
}

function get_tileSource(tileSource,viewer,xml_url,image_url)
{
    $.ajax({
    type:"get",
    url:xml_url,
    data:{},
    dataType:"xml",
    success:function(data){
        tileSource["Image"]["Overlap"]  = data.getElementsByTagName("Image")[0].getAttribute("Overlap");
        tileSource["Image"]["TileSize"] = data.getElementsByTagName("Image")[0].getAttribute("TileSize");
        tileSource["Image"]["Format"]   = data.getElementsByTagName("Image")[0].getAttribute("Format");
        tileSource["Image"]["Size"]["Height"] = data.getElementsByTagName("Size")[0].getAttribute("Height");
        tileSource["Image"]["Size"]["Width"]  = data.getElementsByTagName("Size")[0].getAttribute("Width");
        tileSource["Image"]["Url"] = image_url;
        viewer.open(tileSource);
    }
   })
}

function sync_tab(){
    if(!IS_sync){
        IS_sync = true;
        viewers.forEach(function (viewer) {

            var changeHandler = function () {
                if (leadingViewer && self.leadingViwer !== viewer) {
                    return;
                }
    
                leadingViewer = viewer;
                viewers.forEach(function (viewer_now) {
                    if (viewer_now === viewer) {
                        return;
                    }
    
                    viewer_now.viewport.zoomTo(viewer.viewport.getZoom());
                    viewer_now.viewport.panTo(viewer.viewport.getCenter());
                });
    
                leadingViewer = null;
            };
    
            viewer.addHandler('zoom', function () {
                changeHandler();
            });
    
            viewer.addHandler('pan', function () {
                changeHandler();
            });
        });
    }
    else{
        IS_sync = false;
        viewers.forEach(function (viewer) {
            viewer.removeAllHandlers('zoom');
            viewer.removeAllHandlers('pan');
        });
    }
}

function get_next(){
    date1 = new Date();
    $.ajax({
        type:"post",
        url:"/get_next/",
        //async : false,
        data:{},
        dataType:"json",
        success:function(msg){
            if(msg.state=='fail'){
                alert("!");
            }
            else{
                D_1 = msg.device1;
                D_2 = msg.device2;
                CO_1 = msg.co1;
                CO_2 = msg.co2;
                pho = msg.photo_num;
                url_xml_1 = rootpath+"D"+D_1+"/co"+CO_1+"/xml/"+pho+".xml"
                url_1 = rootpath+"D"+D_1+"/co"+CO_1+"/"+pho+"/";
                url_xml_2 = rootpath+"D"+D_2+"/co"+CO_2+"/xml/"+pho+".xml"
                url_2 = rootpath+"D"+D_2+"/co"+CO_2+"/"+pho+"/";

                get_tileSource(tileSources[0],viewers[0], url_xml_1,url_1);
                get_tileSource(tileSources[1],viewers[1], url_xml_2,url_2);
            }
        },
        error: function(e){
            alert(e.responseText);
        }

       })
}

function get_records(){
    date2 = new Date();
    var result = 0;
    if(check_left){
        result = 0;
    }
    else{
        result = 1;
    }

    var img1 = D_1*10000+1000+pho;
    var img2 = D_2*10000+1000+pho;
    var date3 = parseInt((date2.getTime()-date1.getTime()));

    //alert(img1);
    record_ajax = $.ajax({
        type:"post",
        url:"/record/",
        //async : false,
        data:{img1:img1,img2:img2,result:result,operation:op1,operation_scroll:op2,op_time:date3},
        dataType:"json",
        success:function(msg){
            if(msg.state=='fail'){
                alert("!");
            }
        },
        error: function(e){
            alert(e.responseText);
        }

       })

    op1 = 0;
    op2 = 0;
    return record_ajax;
 }

 function submit(){
    if(check_right || check_left)
    {
        get_records();
    }
    var success =confirm("确定要提交吗？");
    if(success){
        $.ajax({
            type:"post",
            url:"/submit/",
            data:{screen_width:screen.width,screen_height:screen.height,window_width:window.innerWidth,window_height:window.innerHeight,screen_colorDepth:screen.colorDepth},
            dataType:"json",
            success:function(msg){
                if(msg.state == 'ok'){
                    alert("提交成功！");
                    window.location ="/index/";
                }
            }
           })
    } 
}


})