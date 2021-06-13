$(document).ready(function(){
    $('.categories .category').click(function(){
        $(this).addClass('active-category').siblings().removeClass('active-category');;
    })
});