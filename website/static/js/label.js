var img_num = 6;
var col_num = 3;




var root_prefixUrl = static_root + "files/images/";
var rootpath = static_root + "files/photo/";
$("#row1").height(($("#row1").width()-col_num*30)/((4*col_num)/3));
$("#row2").height(($("#row2").width()-col_num*30)/((4*col_num)/3));

var i;
var tileSource = new Array();
var viewer = new Array();
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
    gestureSettingsMouse:{clickToZoom:false},
}

for(i = 0;i<img_num;i++){
    tileSource[i] = new OpenSeadragon.TileSource;
    tileSource[i] = {
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
    viewer[i] = OpenSeadragon(option);
}


D_array = new Array("1","2","3", "4","6","7");
pho = 1;

for(i = 0;i<img_num;i++){
    imgid = i+1;
    url_xml = rootpath+"D"+D_array[i]+"/co4/xml/"+pho+".xml"
    url = rootpath+"D"+D_array[i]+"/co4/"+pho+"/";
    get_tileSource(tileSource[i],viewer[i], url_xml,url);
}

$("#nextimg").click(function(){
    pho++;
    for(i = 0;i<img_num;i++){
        imgid = i+1;
        url_xml = rootpath+"D"+D_array[i]+"/co4/xml/"+pho+".xml"
        url = rootpath+"D"+D_array[i]+"/co4/"+pho+"/";
        get_tileSource(tileSource[i],viewer[i], url_xml,url);
    }
})

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
