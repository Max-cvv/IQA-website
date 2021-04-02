var count = 3;
var node1 = document.getElementById("imgtable");
if(!node1){
    alert("111");
}
node_tr = node1.cloneNode(true);

node_tr.childNodes[1].childNodes[0].src = "photo/1/"+"3"+".jpg";
node_tr.childNodes[3].childNodes[0].src = "photo/1/"+"4"+".jpg";
function addimg(){
    var node1 = document.getElementById("imgtable");
    node_tr = node1.cloneNode(true);
    

    var liftimg = count*2-1;
    var rightimg= count*2;

    node1.parentNode.appendChild(node_tr);
    
    node_tr.childNodes[1].childNodes[0].src = "photo/1/"+liftimg+".jpg";
    node_tr.childNodes[3].childNodes[0].src = "photo/1/"+rightimg+".jpg";
/*
    var img1 = new Image(); 
    img1.src = "photo/1/"+(liftimg+2)+".jpg";
    var img2 = new Image(); 
    img2.src = "photo/1/"+(liftimg+3)+".jpg";
*/
    
    window.location.href = '#but';

    count = count+1;
}