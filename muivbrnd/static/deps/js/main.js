$(document).ready(function () {
    const scrollers = document.querySelectorAll(".scroller");
    
    if (!window.matchMedia("(prefers-reduced-motion: redice)").matches) {
        addAnimation();
    }
    
    function addAnimation() {
        scrollers.forEach(scroller => {
            scroller.setAttribute("data-animated", true);
    
            const scrollerInner = scroller.querySelector(".sc-inner");
            const scrollerContent = Array.from(scrollerInner.children);
    
            scrollerContent.forEach(item => {
                const duplicatedItem = item.cloneNode(true);
                duplicatedItem.setAttribute('aria-hidden', true);
                scrollerInner.appendChild(duplicatedItem);
            })
        })
    }
    
    var succesMessage = $('#jq-notification');

    $(document).on("click", ".add-to-cart", function(e) {
        e.preventDefault();
        
        var goodsInCartCounts = $('#cart-tot-count');
        var cartCount = parseInt(goodsInCartCounts.text() || 0);

        var product_id = $(this).data('product-id');

        var add_to_cart_url = $(this).attr('href');

        $.ajax({
            type: 'POST',
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {

                succesMessage.html(data.message);
                $("#js-alert-box").addClass('notif-box-op');
                succesMessage.fadeIn(400);

                setTimeout( function () {
                    succesMessage.fadeOut(400);
                    $("#js-alert-box").removeClass('notif-box-op');
                    $("#js-alert-box").addClass('notif-box-close');
                }, 4000);
                clearTimeout();
                setTimeout(function() {
                    $('#jq-notification').empty();
                    $("#js-alert-box").removeClass('notif-box-close');
                }, 4500);
                clearTimeout();
                
                cartCount++;
                goodsInCartCounts.text(cartCount);

                var cartItemsContainer = $('#jq-cart-items-container');
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function(data) {
                console.log('Ошибка при добавлении в корзину');
            },
        });

    });

    $(document).on("click", ".remove-from-cart", function(e) {
        e.preventDefault();
        
        var goodsInCartCounts = $('#cart-tot-count');
        var cartCount = parseInt(goodsInCartCounts.text() || 0);

        var cart_id = $(this).data('cart-id');

        var remove_from_cart_url = $(this).attr('href');

        $.ajax({
            type: 'POST',
            url: remove_from_cart_url,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {

                succesMessage.html(data.message);
                $("#js-alert-box").addClass('notif-box-op');
                succesMessage.fadeIn(400);

                setTimeout( function () {
                    succesMessage.fadeOut(400);
                    $("#js-alert-box").removeClass('notif-box-op');
                    $("#js-alert-box").addClass('notif-box-close');
                }, 4000);
                clearTimeout();
                setTimeout(function() {
                    $('#jq-notification').empty();
                    $("#js-alert-box").removeClass('notif-box-close');
                }, 4500);
                clearTimeout();
                
                cartCount -= data.quantity_deleted;
                goodsInCartCounts.text(cartCount);

                var cartItemsContainer = $('#jq-cart-items-container');
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function(data) {
                console.log('Ошибка при удалении товара из корзины');
            },
        });

    });

    $(document).on("click", ".decrement", function() {
        var url = $(this).data('cart-change-url');
        var cartID = $(this).data('cart-id');
        var $input = $(this).closest('.cil-pl-mi').find('.val-number');
        var currentValue = parseInt($input.val());

        if (currentValue >= 1) {
            $input.val(currentValue - 1);

            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    $(document).on("click", ".increment", function() {
        var url = $(this).data('cart-change-url');
        var cartID = $(this).data('cart-id');
        var $input = $(this).closest('.cil-pl-mi').find('.val-number');
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {

                succesMessage.html(data.message);
                $("#js-alert-box").addClass('notif-box-op');
                succesMessage.fadeIn(400);

                setTimeout( function () {
                    succesMessage.fadeOut(400);
                    $("#js-alert-box").removeClass('notif-box-op');
                    $("#js-alert-box").addClass('notif-box-close');
                }, 4000);
                clearTimeout();
                setTimeout(function() {
                    $('#jq-notification').empty();
                    $("#js-alert-box").removeClass('notif-box-close');
                }, 4500);
                clearTimeout();

                var goodsInCartCounts = $('#cart-tot-count');
                var cartCount = parseInt(goodsInCartCounts.text() || 0);
                cartCount += change;
                goodsInCartCounts.text(cartCount);

                var cartItemsContainer = $('#jq-cart-items-container');
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function(data) {
                console.log('Ошибка при удалении товара из корзины');
            },
        });

    }

    $(document).on("click", '#jq-cart-btn', function() {
        $('#mcc-control').css('visibility', 'visible');
    });

    $(document).on("click", '#cbc-btn-id', function() {
        $('#mcc-control').css('visibility', 'hidden');
    });

    var notification = $('#notification');
    if (notification.length > 0) {
        $('#js-alert-box').addClass('notif-box-op');
        setTimeout(function () {
            $('#js-alert-box').removeClass('notif-box-op');
            $('#js-alert-box').addClass('notif-box-close');
        }, 4000);
        clearTimeout();
        setTimeout(function() {
            notification.empty();
            $('#js-alert-box').removeClass('notif-box-close');
        }, 4500);
        clearTimeout();
    }
});