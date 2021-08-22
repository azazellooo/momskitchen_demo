TYPES = []
function addExtra(event){
	event.stopPropagation()
    let block = document.getElementById('selects')
    let add = document.getElementById('add')
    TYPES = JSON.parse(document.getElementById('types').textContent);
    add.style.visibility = 'hidden'
	$("<div/>").attr({id:'selectBlock'}).appendTo(block)
	$("<input/>").attr({type: 'text', id:'comment', value:
        'Комментарий', class:'form-control w-75 p-3', name:('comment' + TYPES.length)}).appendTo('#selectBlock');
    $("<input/>").attr({type: 'number', id:'pricing', value:
        '0', class:'form-control mt-4 w-75 p-3', name:('pricing' + TYPES.length)}).appendTo('#selectBlock');
    $("<select/>").attr({id:TYPES.length, name: TYPES.length}).appendTo('#selectBlock');
    let select = document.getElementById(TYPES.length)
	select.classList.add('form-control')
	select.classList.add('w-75')
	select.classList.add('p-3')
	select.classList.add('mt-4')
    for (let i of TYPES) {
        let option = document.createElement('option')
        option.value = i
        option.innerHTML = i
        select.appendChild(option)

    }
    $("<button class='btn btn-warning m-1'>+</button>").attr({type:'submit', onclick:" return addExtraBtn(event);"}).appendTo('#selectBlock');
    $("<button class='btn btn-warning m-1'>-</button>").attr({type:'submit', onclick:" return removeExtraBtn(event);"}).appendTo('#selectBlock');
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
		 $("<input/>").attr({type: 'text', id:'comment1', class:'form-control mt-4 w-75 p-3', value:
        'Комментарий', name:('comment' + TYPES.length)}).appendTo('#selectBlock1');
    	 $("<input/>").attr({type: 'number', id:'pricing1', class:'form-control mt-4 w-75 p-3', value:
        '0', name:('pricing' + TYPES.length)}).appendTo('#selectBlock1');
    	 $("<select/>").attr({id:TYPES.length, name: TYPES.length}).appendTo('#selectBlock1');
		 let select1 = document.getElementById(TYPES.length)
		select1.classList.add('form-control')
		select1.classList.add('w-75')
		select1.classList.add('p-3')
		select1.classList.add('mt-4')
		 for (let i of TYPES) {
			 let option = document.createElement('option')
			 option.value = i
			 option.innerHTML = i
			 select1.appendChild(option)
		 }
		 $("<button class='btn btn-warning m-1'>+</button>").attr({ onclick:"return addExtraBtn(event);"}).appendTo('#selectBlock1');
		 $("<button class='btn btn-warning m-1'>-</button>").attr({type:'submit', onclick:" return removeExtraBtn(event);"}).appendTo('#selectBlock1');
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