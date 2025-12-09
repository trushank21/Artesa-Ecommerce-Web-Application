// $('#slider1, #slider2, #slider3').owlCarousel({
//     loop: true,
//     margin: 20,
//     responsiveClass: true,
//     responsive: {
//         0: {
//             items: 1,
//             nav: false,
//             autoplay: true,
//         },
//         600: {
//             items: 3,
//             nav: true,
//             autoplay: true,
//         },
//         1000: {
//             items: 5,
//             nav: true,
//             loop: true,
//             autoplay: true,
//         }
//     }
// });



//   $('#slider1').owlCarousel({
//       loop:true,
//       margin:10,
//       nav:true,
//       dots:false,
//       autoplay:true,
//       autoplayTimeout:2500,
//       responsive:{
// 0:{
//               items:2       // <-- MOBILE (0px+) will show 2 items
//           },
//           576:{
//               items:2       // <-- Small phones
//           },
//           768:{
//               items:3       // <-- Tablets
//           },
//           992:{
//               items:4       // <-- Desktop
//           }
//       }
//   });

// $("#slider1").owlCarousel({
//     loop: true,
//     margin: 10,
//     nav: true,
//     navText: [
//         '<i class="fa fa-chevron-left"></i>',
//         '<i class="fa fa-chevron-right"></i>'
//     ],
//     responsive: {
//         0: {
//             items: 2
//         },
//         600: {
//             items: 3
//         },
//         1000: {
//             items: 5
//         }
//     }
// });






$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    $.ajax({
        type:'GET',
        url:'/pluscart',
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('total_amount').innerText=data.total_amount
        }
    })
});



$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    $.ajax({
        type:'GET',
        url:'/minuscart/',
        
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("VISIBILITY RECEIVED:", data.visi);
            eml.innerText=data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('total_amount').innerText=data.total_amount
            if (data.visi === "none") {
                $('#placeorder').hide();      // hide
            } else {
                $('#placeorder').show();      // show
            }
        }
        
    });
});


// $('.remove-cart').click(function(){
//     var id = $(this).attr("pid");
//     var eml=this
//     $.ajax({
//         type:'GET',
//         url:'/removecart',
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             document.getElementById('amount').innerText=data.amount
//             document.getElementById('total_amount').innerText=data.total_amount
//             eml.parentNode.parentNode.parentNode.parentNode.remove()
//         }
//     });




$('.remove-cart').click(function(e){
    e.preventDefault();
    var id = $(this).attr("pid");
    var eml = this;

    $.ajax({
        type: 'GET',
        url: '/removecart',
        data: { prod_id: id },
        success: function(data){
            // Update amounts
            $('#amount').text(data.amount);
            $('#total_amount').text(data.total_amount);

            // Update navbar cart count
            $('#cartCount').text(data.cart_count);

            if(data.cart_count == 0){
                // If cart is empty, replace cart HTML dynamically
                $('#cart-container').html(`
                    <div class="text-center my-5">
                        <h3>You have no products in your cart</h3>
                        <img src="/static/app/images/emptycart.png" class="img-fluid img-thumbnail w-25" alt="Empty Cart">
                    </div>
                `);
                $('#place-order-container').hide()
            } else {
                // Remove the specific item
                $(eml).closest('.cart-item').remove();
            }
        }
    });
});


$("#btnsave").click(function(e) {
            e.preventDefault(); // Stop normal form submit

            let name = $("#yname").val();
            let email = $("#eaddress").val();
            let message = $("#msg").val();
            let csrf = $("input[name=csrfmiddlewaretoken]").val();

            // Simple Validation
            if(name == "" || email == "" || message == ""){
                alert("All fields are required!");
                return;
            }

            $.ajax({
                url: "",
                method: "POST",
                data: {
                    your_name: name,
                    email_address: email,
                    message: message,
                    csrfmiddlewaretoken: csrf
                },

                success: function(data) {
                    if(data.status === "save"){
                        alert("Message Sent Successfully!");

                        // Clear form
                        $("#yname").val("");
                        $("#eaddress").val("");
                        $("#msg").val("");
                    }
                }
            });

});