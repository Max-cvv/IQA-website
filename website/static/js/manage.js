/*
$('.affix ul li a').click(function(e){
    e.preventDefault();
    //修改li的active的位置
    $(this).parent().addClass('active').siblings('.active').removeClass('active');
    //修改右侧主体中的div的active的位置
    var id = $(this).attr('href');
    $(id).addClass('active').siblings('.active').removeClass('active');
   });
*/

window.onload = function(){
    var list = document.getElementById("list");
    var list_ = list.getElementsByTagName("li");
    var content = document.getElementById("right").getElementsByTagName("div");

    for(var i = 0; i < list_.length; i++) {
        var button = list_[i].getElementsByTagName("a")[0];
        button.index=i; 
        button.onclick = function(){
            //this.parentNode.className = "active";
            for(var j = 0; j < content.length; j++){
                content[j].className = "";
            }
            content[this.index].className = "active";
        }
    }
}
