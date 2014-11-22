(function($) {
   $(".updater").click(function(event){
       var me = $(this);
       me.button('loading');

       var vid = me.data( "vid" );
       var op = me.data( "operazione" );
       var tipo = me.data( "tipo" );

       var votiCnt = $('#voti-'+tipo+'-'+vid);
       var decBtn = $("#updater-"+tipo+"-"+vid+"-dec-btn");
       var voti = parseInt(votiCnt.text());

       console.log('voti: '+voti);
       console.log('op: '+op);
       console.log('voti: '+voti);

       if (voti == 0 && op == 'dec') {
           console.log('----------------');
           me.button('reset');
           me.prop("disabled", true);
       } else {
           $.ajax({
               type: "POST",
               url: _url,
               data: {
                   csrfmiddlewaretoken: _token,
                   'vid': vid,
                   'op': op,
                   'tipo': tipo
               },
               success: function (data) {
                   me.button('reset');

                   votiCnt.text(data);
                   voti = parseInt(data);
               },
               error: function () {
                   me.button('reset');
               },
               complete: function (data) {
                   me.button('reset');
                   /*
                   if (voti == 0) {
                       decBtn.prop("disabled", true);
                   } else {
                       decBtn.prop('disabled', false);
                   }*/
               },
               timeout: 20000

           });
       }
        return false;
   });
})(jQuery);