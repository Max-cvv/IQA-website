$(function(){

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


