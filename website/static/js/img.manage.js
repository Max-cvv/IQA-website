var tileSource1 = new OpenSeadragon.TileSource;
var tileSource2 = new OpenSeadragon.TileSource;
var viewer1;
var viewer2;
leadingViewer = null;
var IS_sync = false;
var flag = 0;
var op1 = 0, op2 = 0;
var check_left = false;
var check_right = false;
var D_1,D_2;
var pho;
var date1,date2;
var rootpath = static_root + "files/photo/";
var root_prefixUrl = static_root + "files/images/";
window.onload = function()
{
    //jQuery('#last').hide();
    date1 = new Date();
    tileSource1 = 
    {
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
    tileSource2 = 
    {
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
    viewer1 = OpenSeadragon({
        id:  "img1",
        prefixUrl: root_prefixUrl,
        debugMode: true, //开启调试模式
        //debugGridColor:'#1B9E77', //调试模式下网格的颜色
        minZoomLevel: 0.5,  //最小允许放大倍数
        showNavigator:true,
        navigatorOpacity:1,
        minPixelRatio:0.5,
        minZoomImageRatio:0,
        //controlsFadeDelay:100,
        //controlsFadeLength:0,
        showZoomControl:false,
        showFullPageControl:false,
        gestureSettingsMouse:{clickToZoom:false},
    });
    viewer2 = OpenSeadragon({
        id:  "img2",
        prefixUrl: root_prefixUrl,
        //debugMode: true, //开启调试模式
        //debugGridColor:'#1B9E77', //调试模式下网格的颜色
        minZoomLevel: 0.5,  //最小允许放大倍数
        showNavigator:true,
        navigatorOpacity:1,
        //controlsFadeDelay:100,
        //controlsFadeLength:300,
        showZoomControl:false,
        showFullPageControl:false,
        gestureSettingsMouse:{clickToZoom:false},
    });
    //jQuery('#last').hide();
    viewer_array = Array(viewer1, viewer2);
    //D_1 = randomNum(1,7);
    //D_2 = randomNum(1,7);
    //while(D_2 == D_1){
    //    D_2 = randomNum(1,7);
    //}

    get_next();
    var op_log1 = function(){
        op1 = op1 + 1;
    }

    var op_log2 = function(){
        op2 = op2 + 1;
    }


    viewer1.addHandler( 'canvas-drag-end', op_log1);
    viewer1.addHandler( 'canvas-scroll', op_log2);
    
    viewer2.addHandler( 'canvas-drag-end', op_log1);
    viewer2.addHandler( 'canvas-scroll', op_log2);
    sync_tab(); 
}


function sync_tab(){
    if(!IS_sync){
        IS_sync = true;
        viewer_array.forEach(function (viewer) {

            var changeHandler = function () {
                if (leadingViewer && self.leadingViwer !== viewer) {
                    return;
                }
    
                leadingViewer = viewer;
                viewer_array.forEach(function (viewer_now) {
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
        viewer_array.forEach(function (viewer) {
            viewer.removeAllHandlers('zoom');
            viewer.removeAllHandlers('pan');
        });
    }
}
 
function test(){
    if(check_right || check_left)
    {
        var record_ajax = get_records();
        $.when(record_ajax).done(function () {
            get_next();
        });
        jQuery('#cover_left').hide();
        jQuery('#cover_right').hide();
        check_right = false;
        check_left = false;
    }
    else{
        get_next();
    } 
   
}
function get_next(){
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
                pho = msg.photo_num;
                url_xml_1 = rootpath+"D"+D_1+"/co1/xml/"+pho+".xml"
                url_1 = rootpath+"D"+D_1+"/co1/"+pho+"/";
                url_xml_2 = rootpath+"D"+D_2+"/co1/xml/"+pho+".xml"
                url_2 = rootpath+"D"+D_2+"/co1/"+pho+"/";

                get_tileSource(tileSource1,viewer1, url_xml_1,url_1);
                get_tileSource(tileSource2,viewer2, url_xml_2,url_2);
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

    date1 = new Date();
    op1 = 0;
    op2 = 0;
    return record_ajax;
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

function ck_left(){
    if(!check_left&&!check_right){
        jQuery('#cover_left').show();
        check_left = true;
    }
    else if(check_left){
        jQuery('#cover_left').hide();
        check_left = false;
    }
    else{
        jQuery('#cover_left').show();
        jQuery('#cover_right').hide();
        check_left = true;
        check_right = false;
    }
}
function ck_right(){
    if(!check_left&&!check_right){
        jQuery('#cover_right').show();
        check_right = true;
    }
    else if(check_right){
        jQuery('#cover_right').hide();
        check_right = false;
    }
    else{
        jQuery('#cover_right').show();
        jQuery('#cover_left').hide();
        check_right = true;
        check_left = false;
    }
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


function randomNum(minNum,maxNum){ 
    switch(arguments.length){ 
        case 1: 
            return parseInt(Math.random()*minNum+1,10); 
        break; 
        case 2: 
            return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10); 
        break; 
            default: 
                return 0; 
            break; 
    } 
} 
