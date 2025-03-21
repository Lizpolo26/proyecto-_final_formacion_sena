(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').css('top', '0px');
        } else {
            $('.sticky-top').css('top', '-100px');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Date and time picker
    $('.date').datetimepicker({
        format: 'L'
    });
    $('.time').datetimepicker({
        format: 'LT'
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 25,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    
})(jQuery);


function toggleCart() {
    // Lógica para mostrar/ocultar el carrito de compras
    const cart = document.getElementById('cart');
    if (cart.style.display === 'none' || cart.style.display === '') {
        cart.style.display = 'block';
    } else {
        cart.style.display = 'none';
    }
}



// Reserva
document.addEventListener("DOMContentLoaded", function () {
    const fechaInput = document.getElementById("fecha");
    const horaInput = document.getElementById("hora");

    // Restringe la selección de fechas anteriores a la actual
    const hoy = new Date().toISOString().split("T")[0];
    fechaInput.setAttribute("min", hoy);

    // Restringe la selección de horas fuera del rango 17:00 - 23:00
    function validarHora() {
        if (!horaInput.value) return; // Evita errores si el campo está vacío

        let horaSeleccionada = parseInt(horaInput.value.split(":")[0]);

        if (horaSeleccionada < 17 || horaSeleccionada > 23) {
            Swal.fire({
                icon: "error",
                title: "Hora no válida",
                text: "Por favor, selecciona una hora entre las 17:00 y las 23:00.",
                confirmButtonText: "Entendido"
            });
            horaInput.value = ""; // Borra la hora inválida
        }
    }

    // Validar fecha para evitar errores de evento no definido
    function validarFecha() {
        if (fechaInput.value < hoy) {
            fechaInput.value = hoy;
        }
    }

    fechaInput.addEventListener("change", validarFecha);
    horaInput.addEventListener("change", validarHora); // Usa 'change' para evitar errores
});