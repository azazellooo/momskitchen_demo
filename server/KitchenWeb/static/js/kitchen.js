TYPES = []
function addExtra(event){
	event.stopPropagation()
    let block = document.getElementById('selects')
    let add = document.getElementById('add')
    TYPES = JSON.parse(document.getElementById('types').textContent);
    add.style.visibility = 'hidden'
	$("<div/>").attr({id:'selectBlock'}).appendTo(block)
	$("<input/>").attr({type: 'text', id:'comment', value:
        'Comment', name:('comment' + TYPES.length)}).appendTo('#selectBlock');
    $("<input/>").attr({type: 'number', id:'pricing', value:
        '20', name:('pricing' + TYPES.length)}).appendTo('#selectBlock');
    $("<select/>").attr({id:TYPES.length, name: TYPES.length}).appendTo('#selectBlock');
    let select = document.getElementById(TYPES.length)
    for (let i of TYPES) {
        let option = document.createElement('option')
        option.value = i
        option.innerHTML = i
        select.appendChild(option)
    }
    $("<button><i class=\"fas fa-plus-circle\"></i></button>").attr({type:'submit', onclick:" return addExtraBtn(event);"}).appendTo('#selectBlock');
    $("<button><i class=\"fas fa-minus-circle\"></i></button>").attr({type:'submit', onclick:" return removeExtraBtn(event);"}).appendTo('#selectBlock');
}

 function  addExtraBtn(event) {
	event.stopPropagation()
	if (TYPES.length > 1){
		 let select = document.getElementById(TYPES.length)
		 let selected = select.value
		 let block = document.getElementById('selects')
		 let toRemove = TYPES.indexOf(parseFloat(selected))
		 TYPES.splice(toRemove, 1)
		 $("<div/>").attr({id:'selectBlock1'}).appendTo(block)
		 $("<input/>").attr({type: 'text', id:'comment1', value:
        'Comment', name:('comment' + TYPES.length)}).appendTo('#selectBlock1');
    	 $("<input/>").attr({type: 'number', id:'pricing1', value:
        '20', name:('pricing' + TYPES.length)}).appendTo('#selectBlock1');
    	 $("<select/>").attr({id:TYPES.length, name: TYPES.length}).appendTo('#selectBlock1');
		 let select1 = document.getElementById(TYPES.length)
		 for (let i of TYPES) {
			 let option = document.createElement('option')
			 option.value = i
			 option.innerHTML = i
			 select1.appendChild(option)
		 }
		 $("<button><i class=\"fas fa-plus-circle\"></button>").attr({ onclick:"return addExtraBtn(event);"}).appendTo('#selectBlock1');
		 $("<button><i class=\"fas fa-minus-circle\"></i></button>").attr({type:'submit', onclick:" return removeExtraBtn(event);"}).appendTo('#selectBlock1');
		 return false
	}
	else {
		window.alert("Больше типов нет!")
		return false
	}
 }

 function removeExtraBtn(event){
	 event.stopPropagation()
	 let toRemove = event.currentTarget.parentNode
	 toRemove.remove()
	 if ( $('.selects').children().length == 0 ) {
	 	let add = document.getElementById('add')
		 add.style.visibility = 'visible'
}
}