var ALERTS = false;
var mobile = false;
var AJAXING = false;
var SUCCESS = false;
var NOTIFCOUNT = 0;

$(document).ready(function () {
});

function ajaxWrapper(type, url, data, returnFunc, context){
    SUCCESS = false;
    AJAXING = true;

    $.ajax({
        type: type,
        url: url,
        data: data,
        success: function (value) {
            AJAXING = false;
            SUCCESS = true;
            console.log(value);

            keys = Object.keys(value);
            this.setState({
                [keys[0]]: value[keys[0]]
            })

        }.bind(context),
        error: function(xhr, status, error) {
            AJAXING = false;
            console.log(xhr.responseText);
        }
    });
}

function ajaxFileWrapper(type, url, data, returnFunc, container){
    SUCCESS = false;
    AJAXING = true;

    $.ajax({
        type: type,
        url: url,
        data: data,

        dataType: 'json',
        processData: false,
        contentType: false,

        success: function (value) {
            AJAXING = false;
            SUCCESS = true;
            returnFunc(value, container);
        },
        error: function(xhr, status, error) {
            AJAXING = false;
            console.log(xhr.responseText);
        }
    });
}


function showNotif(container, msg, color, btn){
    NOTIF = true;
    if (color == undefined){color = 'warning';}
    var num = NOTIFCOUNT;
    NOTIFCOUNT += 1;

    var notif = $('<p class="showInput col-xs-12"></p>');
    notif.append('<div class="row transitions alertbox" num="'+num+'" style="height:0px;overflow:;overflow:hidden;opacity:0;"></div>');
    notif.append('<div class="col-xs-12 alert alert-'+color+'" role="alert" style="margin-bottom:0px;">'+msg+'</div>');

    $(container).append(notif);
}




function closeCover(){
    $('.cover .floating-cover-content').html('');

	$('.cover').hide();
	$('body>div').not('.cover').show();
	$('body').css('overflow','scroll');
}
function openCover(){
	$('.cover').height($(window).height());
	$('body').css('overflow','hidden');
	$('.cover').show();
}
function openMobileCover(){
	if ($('.cover').height() < $(window).height()){
		$('.cover').height($(window).height());
	} else {$('.cover').height('auto');}

	$('body>div').not('.cover').hide();
	$('.cover').show();
}

function loadCoverContent(url, data){ajaxWrapper('get',url,data,addCoverContent);}

function addCoverContent(value){
	console.log(value);
	$('.cover .cover-inner .cover-content').html(value);

	$('.cover .floating-cover-content').append($('.cover .cover-inner .cover-content .floatingelement'));

	if (mobile){
		openMobileCover();
	}
	else {
		openCover();
	}
	//$('html, body').animate({ scrollTop: 0 }, 0);
}

function appendCoverContent(value){
	var current = $('.cover .cover-inner .cover-content');
	current.removeClass('cover-content');
	current.addClass('previous-cover-content');

    //This should be included in the queue functionality
    $('.cover .floating-cover-content').html('');

	$('.cover .cover-inner').append('<div class="cover-content"></div>');
	addCoverContent(value);
}
function popCoverContent(){
    $('.cover .floating-cover-content').html('');

	if ($('.cover .cover-inner .previous-cover-content').length > 0){
		$('.cover .cover-inner .cover-content').remove();
		var previous = $('.cover .cover-inner .previous-cover-content').last();
		previous.addClass('cover-content');
		previous.removeClass('previous-cover-content');
	} else {
		closeCover();
	}
}
