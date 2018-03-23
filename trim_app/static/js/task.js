document.addEventListener("DOMContentLoaded", function(){

    var button = document.getElementById("button");
    button.addEventListener("click", function(event){
       var dt = new Date();
       document.write(dt);
    });
});
