function boxes(){
	var list=document.querySelectorAll("div.plotdiv");
	for (var i in list) {
		var box=$('<input type="checkbox"/>');
		box.attr('id', i.toString());
		$('#'+list[i].id).append(box);
	}
}

setTimeout(boxes,60000);

function print(){
	var inputList=document.querySelectorAll("input");
	var scriptList=$("script");
	for (var i in inputList) {
		if (inputList[i].checked) {
			var number = inputList[i].id;
			var s=scriptList[parseInt(number)+2].innerHTML;
			var id=s.substring(s.indexOf('legends')+13,s.indexOf('legends')+24);
			console.log(id);
		}
	}
}

function ids() {
	var inputList=document.querySelectorAll("input");
	var scriptList=$("script");
	for (i = 0; i < inputList.length; i++){
			var s=scriptList[i+2].innerHTML;
			var id=s.substring(s.indexOf('legends')+13,s.indexOf('legends')+24);
			var p=$("<p></p>");
			p.text(id);
			p.insertAfter($("#"+i));
		}
	}