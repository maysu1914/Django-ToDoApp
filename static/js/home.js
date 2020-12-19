$( document ).ready(function() {

    // to change arrow direction
    $('.fa-chevron-down, .fa-chevron-up').click(function(){
        if ($(this).hasClass('fa-chevron-down')){
            $(this).removeClass('fa-chevron-down');
            $(this).addClass('fa-chevron-up');
            getItemsByListId( $(this).attr('data-list-id') );
        } else {
            $(this).removeClass('fa-chevron-up');
            $(this).addClass('fa-chevron-down');
        }
    });
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
    $('.add-new-item-button').click(function(){
        let action = $(this).attr("data-form");
        $('#add-new-item-form').attr("action", action);
    });

    function setItemsByListId( list_id, datas ){
        target_table_id = "datas-" + list_id.toString();
        table_element = document.getElementById(target_table_id);
        target_body = table_element.getElementsByClassName('data-body')[0];
        loading_icon = document.getElementById('loading-icon-'+list_id.toString());
        console.log(loading_icon);
        loading_icon.hidden = true;
        if ( datas.length ){
            table_element.hidden = false;
        } else {
            table_element.hidden = true;
        }
        sample_data_row = table_element.getElementsByClassName('sample-data-row')[0];

        $('.data-row-'+list_id.toString()).remove();

        for ( data of datas ){
            new_data_row = sample_data_row.cloneNode(true);
            new_data_row.hidden = false;
            new_data_row.className = 'data-row-'+list_id.toString();
            fields = new_data_row.getElementsByTagName('TD');
            fields[0].innerHTML = data.fields.name;
            fields[1].innerHTML = data.fields.status;
            fields[2].innerHTML = data.fields.created;
            fields[3].innerHTML = data.fields.deadline;
            fields[4].innerHTML = data.fields.description;
            fields[5].getElementsByTagName('A')[0].setAttribute("data-item-id", data.pk.toString());
            fields[5].getElementsByTagName('A')[1].setAttribute("data-item-id", data.pk.toString());
            target_body.appendChild(new_data_row);
        }
    }

    function getItemsByListId( list_id ){
        options =  getItemOptions(document.getElementById('list-'+list_id.toString()));
        console.log(options);
        var base_url = window.location.origin;
        let url = new URL(base_url+'/get_items/' + list_id.toString());
        url.searchParams.set('status', options.status);
        url.searchParams.set('sort', options.sort);

        $.get( url , function( items ) {
            try {
                datas = JSON.parse(items.result);
                setItemsByListId( list_id, datas.reverse() )
            } catch {
                console.log(items.result)
                return false;
            }
        });
    }

    function getItemOptions(element){
        options = {'status':'All','sort':'deadline'}
        for(el of element.getElementsByTagName("INPUT")){
            if(el.checked){
                options[el.name] = el.value;
            }
        }
        return options;
    }

    $('.statusing, .sorting').click(function(){
        let pieces = this.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id.split('-');
        let list_id = pieces[pieces.length-1];
        getItemsByListId( list_id );
    })

    // item add
    $( "#add-new-item-form" ).on( "submit", function(e) {
        button = document.getElementById('submit-button')
        default_text= button.innerHTML
        pieces = $(this).attr('action').split('/');
        list_id = pieces[pieces.length-1];
        button.innerHTML = "<i class='fas fa-circle-notch fa-spin'></i>";
        var dataString = $(this).serialize();

        $.ajax({
              type: "POST",
              url: $(this).attr('action'),
              data: dataString,
              success: function () {
                button.innerHTML = default_text;
                $('#add-new-item-modal').modal('hide');
                getItemsByListId( list_id );
              },
              error: function($xhr,textStatus,errorThrown){
                button.innerHTML = default_text;
                fields = $xhr.responseJSON;
                for(field in fields.errors){
                    error_place = document.getElementById('id_'+field);
                    form_body = error_place.parentNode;
                    for(let error of fields.errors[field]){
                        sample_error = document.getElementById('sample-error').cloneNode(true);
                        sample_error.hidden = false;
                        sample_error.removeAttribute('id');
                        sample_error.innerHTML = error + sample_error.innerHTML;
                        form_body.innerHTML= sample_error.outerHTML + form_body.innerHTML;
                    }
                }
              }
            });
        e.preventDefault();
    });

    // delete item
    $('body').on('click', 'a.item-delete', function() {
        default_text= this.innerHTML;
        item_id = this.getAttribute("data-item-id");
        pieces = this.parentNode.parentNode.parentNode.parentNode.id.split('-');
        list_id = pieces[pieces.length-1];
//        console.log(list_id);
        this.innerHTML = "<i class='fas fa-circle-notch fa-spin'></i>";

        $.get( 'delete_item/' + item_id.toString(), function() {
            getItemsByListId( list_id );
        });
    });

    //approve item
    $('body').on('click', 'a.item-approve', function() {
        default_text= this.innerHTML;
        item_id = this.getAttribute("data-item-id");
        pieces = this.parentNode.parentNode.parentNode.parentNode.id.split('-');
        list_id = pieces[pieces.length-1];
//        console.log(list_id);
        this.innerHTML = "<i class='fas fa-circle-notch fa-spin'></i>";

        $.get( 'approve_item/' + item_id.toString(), function() {
            getItemsByListId( list_id );
        });
    });
});

