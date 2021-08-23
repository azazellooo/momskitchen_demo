    $(document).ready(function(){
        $("#form input[type='text']").prop("disabled", true);
        $("#id_is_active").prop("disabled",true);
        let username = $( "#form input[type=text]").val();
        localStorage.setItem("username", username);
        let is_active = $( "#form input[type=checkbox]").val();
        localStorage.setItem("is_active", is_active);
        console.log('hjopo')
    });
        function update_button(event){
            event.stopPropagation()
        $("#form input[type='text']").prop("disabled", false);
        $("#id_is_active").prop("disabled", false);
        $("#update_button").remove();
        $("<input/>").attr({type: 'submit', id:'save_button', value:
        'Сохранить', class: 'btn m-3',
            style: 'background: rgb(255,189,114); background: linear-gradient(90deg, rgba(255,189,114,1) 0%, rgba(204,255,0,0.00424168690913862) 40%, rgba(255,161,161,1) 100%);',
            onclick: 'Save(event)'}).appendTo('#form');
        $("<button class='btn btn-warning'>Отменить</button>").attr({type:'submit', id:'cancel_button', onclick:'Cancel(event)'}).appendTo('#update_block');
};
    function Cancel(event){
        window.location.reload()
    }
    function Save(event){
        return true
};
