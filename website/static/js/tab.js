var IS_tab = true


window.onload = function(){
    var userAgentInfo = navigator.userAgent;
    var Agents = ["Android", "iPhone",
      "SymbianOS", "Windows Phone",
      "iPad", "iPod"];
    var flag = false;
    for (var v = 0; v < Agents.length; v++) {
      if (userAgentInfo.indexOf(Agents[v]) > 0) {
          flag = true;
          break;
      }
    }
   if(flag){
        window.location.replace("hello.htm")
        
   }
}


function tab(){

    var node1 = document.getElementById("word");
    var node2 = document.getElementById("input1");
    var node3 = document.getElementById("input2");
    var node4 = document.getElementById("but1");
    if(IS_tab){
        node1.innerHTML="管理员登录";
        node4.innerHTML="返回";
        node2.setAttribute("placeholder","用户名");
        node3.style.display="inline";
        IS_tab=false;
    }
    else{
        node1.innerHTML="请输入邀请码";
        node4.innerHTML="管理员登录";
        node2.setAttribute("placeholder","");
        node3.style.display="none";
        IS_tab=true;
    }
    
   
}