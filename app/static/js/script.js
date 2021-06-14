$(document).ready(function(){
    $('.categories a').click(function(){
        $(this).addClass('active-category').siblings().removeClass('active-category');;
    })
});