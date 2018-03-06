window.onload = function(){
    var star = document.getElementsByTagName('i');
    var oDiv = document.getElementById('starBox');
    var temp = 0;

    for(var i = 0, len = star.length; i < len; i++){
        star[i].index = i;

        star[i].onmouseover = function(){
            clear();
            for(var j = 0; j < this.index + 1; j++){
                star[j].className = 'fas fa-star';

            }
        }

        star[i].onmouseout = function(){
            for(var j = 0; j < this.index + 1; j++){
                star[j].className = 'far fa-star';
            }
            current(temp);
        }

        star[i].onclick = function(){
            temp = this.index + 1;
            console.log('click'+temp)
            document.getElementById('star_rating').value = temp;
            current(temp);
        }
    }
    //清除所有
    function clear(){
        for(var i = 0, len = star.length; i < len; i++){
            star[i].className = 'far fa-star';
        }
    }
    //显示当前第几颗星
    function current(temp){
        for(var i = 0; i < temp; i++){
            star[i].className = 'fas fa-star';
        }
    }
};