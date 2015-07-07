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

function desc(){
	var inputList=document.querySelectorAll("input");
	var scriptList=$("script");
	for (i = 0; i < inputList.length; i++){
		var s=scriptList[i+2].innerHTML;
		var lis=s.split(';');
		
		// video IDs
		var id = s.substring(s.indexOf('legends')+13,s.indexOf('legends')+24);
		var ids = $("<p></p>");
		ids.text(id);
		ids.insertAfter($("#"+i));
			
		// title
		var lis2 = lis[6].split('title');
		var title = lis2[2].substring(4,lis2[2].indexOf(',')-1);
		var t=$("<p></p>");
		t.text(title);
		t.insertAfter($("#"+i));
	
		// frequent words
		var n = lis[6].indexOf('"12pt", "name":');
		var m = lis[6].indexOf('"title": "' + title);
 		var freq = lis[6].substring(n+17,m-3); 
		var f=$("<p></p>");
   	 	f.text(freq);
   	 	f.insertAfter($("#"+i));
	}
}
