$(function(){

function scroll() {
    //var top = $(".div3").offset().top;//获取导航栏变色的位置距顶部的高度
    var scrollTop = $(window).scrollTop();//获取当前窗口距顶部的高度
    //alert(scrollTop);
    if (scrollTop>40) {
        //alert("1");
        $('.navbar-default').css({
            'border-bottom':'1px solid rgb(214, 214, 214)'}
            );
    } else {
        $('.navbar-default').css({
            'border-bottom':'0px solid rgb(214, 214, 214)'}
            );
    }
}
$(window).scroll(function() {
    scroll();
});


$("#form-btn").click(function(){

    
    
    
    var gender = $("[name = 'gender']:checked").val();
    var age = $("[name = 'age']:checked").val();
    var isGlasses = $("[name = 'isGlasses']:checked").val();
    var edu = $("[name = 'edu']:checked").val();
    var pho = $("[name = 'pho']:checked").val();
    var screen = $("#screen").val();
    if(age && isGlasses && gender  && edu && pho){
        $.ajax({
            type:"post",
            url:"/hand_form/",
            //async : false,
            data:{"age":age, "gender":gender, "isGlasses":isGlasses, "edu":edu, "pho":pho, "screen":screen},
            dataType:"json",
            success:function(msg){
                if(msg.state=='fail'){
                    alert("!");
                }
                else{
                    //window.location ="/index/";
                    window.open('/index/');
                }
            },
            error: function(e){
                alert(e.responseText);
            }

        })
    }
    else{
        showModal("提示", "请将必填项填写完整");
    }
    

});


})


