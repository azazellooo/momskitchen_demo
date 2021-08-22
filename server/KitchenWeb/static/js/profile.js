    $(document).ready(function(){
        $("#form input[type='text']").prop("disabled", true);
        $("#id_is_active").prop("disabled",true);
        let username = $( "#form input[type=text]").val();
        localStorage.setItem("username", username);
        let is_active = $( "#form input[type=checkbox]").val();
        localStorage.setItem("is_active", is_active);
    });
        function update_button(event){
            event.stopPropagation()
        $("#form input[type='text']").prop("disabled", false);
        $("#id_is_active").prop("disabled", false);
        $("#update_button").remove();
        $("<input/>").attr({type: 'submit', id:'save_button', value:
        'Сохранить', onclick: 'Save(event)'}).appendTo('#form');
        $("<button>Отменить</button>").attr({type:'submit', id:'cancel_button', onclick:'Cancel(event)'}).appendTo('.form_profile');
        $("#save_button").addClass("btn btn-info")
        $("#cancel_button").addClass("btn btn-info")
};
    function Cancel(event){
        window.location.reload()
    }
    function Save(event){
        return true
};
