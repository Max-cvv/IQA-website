$(function(){


    
       
     //setTimeout(function(){$('#overlay').fadeOut('slow')}, 3000); //设置3秒后覆盖层自动淡出
  


function scroll() {
    var top = $(".div3").offset().top;//获取导航栏变色的位置距顶部的高度
    var scrollTop = $(window).scrollTop();//获取当前窗口距顶部的高度
    //alert(top+scrollTop);
    if (scrollTop < top) {
        $('.navbar').css('opacity', 1);
    } else {
        
        $('.navbar').css('opacity', 0.1);
    }
}
$(window).scroll(function() {
    scroll();
});


$("#form-btn").click(function(){

    
    var age = $("#age").val();
    var job = $("#job").val();
    var gender = $("[name = 'gender']:checked").val();
    var isGlasses = $("[name = 'isGlasses']:checked").val();
    if(age && job && gender && isGlasses){
        $.ajax({
            type:"post",
            url:"/hand_form/",
            //async : false,
            data:{"age":age, "job":job, "gender":gender, "isGlasses":isGlasses},
            dataType:"json",
            success:function(msg){
                if(msg.state=='fail'){
                    alert("!");
                }
                else{
                    code = msg.auth_code;
                    alert(code);
                }
            },
            error: function(e){
                alert(e.responseText);
            }

        })
    }
    else{
        showModal("提示", "请填写完整");
    }
    

});


})


