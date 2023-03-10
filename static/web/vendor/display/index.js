let params = Wolmart.getURLParams(), category = params.category ? params.category : '',
    max_num = params['max_num'] ? params['max_num'] : Number.MAX_SAFE_INTEGER,
    min_num = params['min_num'] ? params['min_num'] : 0

compare = Wolmart.getCookie('compare') ? JSON.parse(Wolmart.getCookie('compare')) : [];

async function renderData(data, site) {
    let shopgrid = "", shoplist = "", no_product = `<li class="no-product">
<p class="alert alert-light alert-info woocommerce-info">No products were found matching your selection.</p>
</li>`, n = 0, x = '', wishlist = '';
    $.each(data, function (index, item) {
        if (item.price) item.price = OSREC.CurrencyFormatter.format(item.price, currency);
        if (item.discount_price) item.discount_price = OSREC.CurrencyFormatter.format(item.discount_price, currency);
        if (site == 'shop') {
            // Shop list & grid Display
            shoplist += ` <div class="product product-list" id="${item.id}"> <figure class="product-media"> <a href="/product/${item.id}"> <img src="${item.image[0]}" alt="Product" width="330" height="338" /> <img src="${item.image[1]}" alt="Product" width="330" height="338" /> </a> <div class="product-action-vertical"> <a href="#" class="btn-product-icon btn-quickview w-icon-search" title="Quick View"></a> </div> ${productCountDown(item)}</figure> <div class="product-details"> <div class="product-cat"> <a href="/products/shop">${item.category}</a> </div> <h4 class="product-name"> <a href="/product/${item.id}">${item.name}</a> </h4> <div class="ratings-container"> <div class="ratings-full"> <span class="ratings" style="width: ${item.review_percentage}%;"></span> <span class="tooltiptext tooltip-top"></span> </div> <a href="/product/${item.id}" class="rating-reviews">(${item.review_count} Reviews)</a> </div>`
            shoplist += item.discount_price && item['discount_duration'] >= new Date() ? `<div class="product-price"> <ins class="new-price">${item.discount_price}</ins><del class="old-price">${item.price}</del> </div> ` : `<div class="product-price">${item.price}</div>`
            shoplist += `<div class="product-desc">
            Ultrices eros in cursus turpis massa cursus mattis. Volutpat ac tincidunt
            vitae semper quis lectus. Aliquam id diam maecenas ultricies…
        </div> <div class="product-action">${Icon(item.id, 'cart', true)} <a href="#" class="btn-product-icon btn-wishlist w-icon-heart" title="Wishlist"></a>${Icon(item.id, 'compare')}</div> </div> </div>`
            shopgrid += `<div class="product-wrap" ><div class="product text-center" id="${item.id}"><figure class="product-media"><a href="/product/${item.id}"> 
        <img src="${item.image[0]}" alt="Product" width="300" height="338" /> </a> ${productCountDown(item)}<div class="product-action-horizontal"> 
        ${Icon(item.id, 'cart')}<a href="#" class="btn-product-icon btn-wishlist w-icon-heart" title="Wishlist"></a> ${Icon(item.id, 'compare')}<a href="#" class="btn-product-icon btn-quickview w-icon-search" title="Quick View"></a> </div> </figure> <div class="product-details"> <div class="product-cat"> <a href="/products/shop">${item.category}</a> </div> <h3 class="product-name"> <a href="/product/${item.id}">${item.name}</a> </h3> <div class="ratings-container"> <div class="ratings-full"> <span class="ratings" style="width: ${item.review_percentage}%;"></span> <span class="tooltiptext tooltip-top"></span> </div> <a href="/product/${item.id}" class="rating-reviews">(${item.review_count} reviews)</a> </div> <div class="product-pa-wrapper">`
            shopgrid += item.discount_price ? `<div class="product-price"> <ins class="new-price">${item.discount_price}</ins><del class="old-price">${item.price}</del> </div> ` : `<div class="product-price">${item.price}</div>`
            shopgrid += `</div> </div> </div> </div>`;
        }
        if (site == 'wishlist') {
            wishlist += `
            <tr id="${item.id}">
                <td class="product-thumbnail" >
                    <div class="p-relative">
                        <a href="/product/${item.id}" class="product-image">
                            <figure>
                                <img src="${item.image[0]}" alt="product" width="300"
                                    height="338">
                            </figure>
                        </a>
                        <button type="submit" class="btn btn-close"><i
                                class="fas fa-times"></i></button>
                    </div>
                </td>
                <td class="product-name">
                    <a href="/product/${item.id}">
                       ${item.name}
                    </a>
                </td>
                <td class="product-price"><ins class="new-price">${item.price}</ins></td>
                <td class="product-stock-status">
                    <span class="wishlist-in-stock">In Stock</span>
                </td>
                <td class="wishlist-action">
                    <div class="d-lg-flex">
                        <a href="#"
                            class="btn btn-quickview btn-outline btn-default btn-rounded btn-sm mb-2 mb-lg-0">Quick
                            View</a>
                        <a class="btn-cart btn btn-dark btn-rounded btn-sm ml-lg-2 ">Add to
                            cart</a>
                    </div>
                </td>
            </tr>`
        }
        // Browse Categories Tree Display

        if (site == 'index') {
            if (n == 3) return false
            x += ` <div class="product-wrapper-1 scroll-product mb-7">
            <div class="title-link-wrapper pb-1 mb-4">
                <h2 class="title ls-normal mb-0">${index}</h2>
                <a href="/products/shop" class="font-size-normal font-weight-bold ls-25 mb-0">More
                    Products<i class="w-icon-long-arrow-right"></i></a>
            </div>
            <div class="row">
                <div class="col-lg-3 col-sm-4 mb-4">
                    <div class="banner h-100 br-sm" style="background-image: url(/static/web/images/demos/demo1/banners/5.jpg); 
                    background-color: #EAEFF3;">
                        <div class="banner-content content-top">
                            <h5 class="banner-subtitle font-weight-normal mb-2">Deals And Promotions</h5>
                            <hr class="banner-divider bg-dark mb-2">
                            <h3 class="banner-title font-weight-bolder text-uppercase ls-25">
                                Trending <br> <span class="font-weight-normal text-capitalize">House
                                    Utensil</span>
                            </h3>
                            <a href="/products/shop"
                                class="btn btn-dark btn-outline btn-rounded btn-sm">shop now</a>
                        </div>
                    </div>
                </div>
                <!-- End of Banner -->
                <div class="col-lg-9 col-sm-8">
                    <div class="swiper-container swiper-theme" data-swiper-options="{
                        'spaceBetween': 20,
                        'slidesPerView': 2,
                        'breakpoints': {
                            '992': {
                                'slidesPerView': 3
                            },
                            '1200': {
                                'slidesPerView': 4
                            }
                        }
                    }">
                    <div class="swiper-wrapper animate row cols-xl-4 cols-lg-3 cols-2">
                ${renderProducts(item)}
                                    </div>
                        <div class="swiper-pagination"></div>
                    </div>
                    <!-- End of Produts -->
                </div>
            </div>
        </div>
        `
            n++
        }

    })
    if (site == 'shop') {
        shopgrid = shopgrid !== "" ? shopgrid : no_product
        shoplist = shoplist !== "" ? shoplist : no_product

        $('#shop-grid').html(shopgrid) && $('#shop-list').html(shoplist);

        document.querySelector('.product-countdown-container') && Wolmart.countDown($('.product').find('.product-countdown'));
        getUser()
    } else {
        $('#category-index').append(x);
        $('#wish-list').append(wishlist);
        if (wishlist != "") {
            $('.wishlist_view').attr('class', 'shop-table wishlist-table')
            let i = $('.wishlist-table').find('thead').removeClass('d-none');
            $('.wishlist-items-wrapper').html(wishlist).removeClass('wishlist-empty').removeClass('wishlist-items-wrapper')
        }
        Wolmart.slider(".swiper-container");
    }
}

function paginate(data) {
    if (data.next || data.previous) $('.toolbox-pagination').show()


    function active(n) {
        if (n == data.current_page) return 'active'
    }

    $('.showing').text(`${((Number(data.size) * Number(data.current_page)) - (Number(data.current_page) + 1))} - ${data.size} of ${data.count}`)
    let x = ''
    x += data.previous ? `<li class="prev"><a ttr="${data.previous}" href='#' class="pagination-link" aria-label="Previous" tabindex="-1" aria-disabled="true"> <i class="w-icon-angle-left"></i> </a></li>` : ''
    for (let i = 1; i <= data.pages; i++) {
        x += (data.current_page - 2) <= i && i <= (data.current_page + 2) ? `<li class="page-item ${active(i)}"><a ttr="/api/product/list?p=${i}" class="page-link pagination-link" href="#">${i}</a></li>` : ''
    }
    x += data.next ? `<li class="next"><a ttr="${data.next}" href='#' class="pagination-link" aria-label="Next"> <i class="w-icon-angle-right"></i></a></li>` : ''
    $('.pagination').html(x)
}

function productCountDown(product) {
    let date = new Date(product.discount_duration)
    if (product.discount_duration && date > new Date()) return `<div class="product-countdown-container"> <div class="product-countdown countdown-compact" data-until="${product.discount_duration} "data-format="DHMS" data-compact="false" data-labels-short="Days, Hours, Mins, Secs"> 00:00:00:00</div> </div> `
    return ``
}

function renderProducts(n) {
    let z = '';
    for (let i = 0; i < n.length; i += 2) {
        let item1 = n[i], item2 = n[i + 1];

        z += `<div class="swiper-slide product-col">`
        z += `<div class="product-wrap product text-center" id="${item1.id}">
        <figure class="product-media">
            <a href="/product/${item1.id}">
                <img src="${item1.image[0]}" alt="Product"
                    width="216" height="243" />
            </a>
            <div class="product-action-vertical">
                ${Icon(item1.id, 'cart')}
                <a href="#" class="btn-product-icon btn-wishlist w-icon-heart"
                    title="Add to wishlist"></a>
                <a href="#" class="btn-product-icon btn-quickview w-icon-search"
                    title="Quickview"></a>
                   <a href="#" class="btn-product-icon btn-cart w-icon-cart" title="Add to cart"></a>
                    
            </div>
            <div class="product-label-group">
                        <label class="product-label label-discount">${Number(item1.discount)}% Off</label>
                    </div>
        </figure>
        <div class="product-details">
            <h4 class="product-name"><a href="/product/${item1.id}">${item1.name}</a>
            </h4>
            <div class="ratings-container">
                <div class="ratings-full">
                    <span class="ratings" style="width: ${item1.review_percentage}%;"></span>
                    <span class="tooltiptext tooltip-top"></span>
                </div>
                <a href="/product/${item1.id}" class="rating-reviews">(5
                    reviews)</a>
            </div>
            <div class="product-price">
                <ins class="new-price">${OSREC.CurrencyFormatter.format(item1.price, currency)}</ins>
            </div>
        </div>
    </div>
    `
        z += item2 ? `
    <div class="product-wrap product text-center" id="${item2.id}">
        <figure class="product-media">
            <a href="/product/${item2.id}">
                <img src="${item2.image[0]}" alt="Product"
                    width="216" height="243" />
            </a>
            <div class="product-action-vertical">
                ${Icon(item2.id, 'cart')}
                <a href="#" class="btn-product-icon btn-wishlist w-icon-heart" title="Wishlist">
                <a href="#" class="btn-product-icon btn-quickview w-icon-search"
                    title="Quickview"></a>
                    <a href="#" class="btn-product-icon btn-cart w-icon-cart" title="Add to cart"></a>
            </div>
        </figure>
        <div class="product-details">
            <h4 class="product-name"><a href="/product/${item2.id}">${item2.name}</a></h4>
            <div class="ratings-container">
                <div class="ratings-full">
                    <span class="ratings" style="width: ${item2.review_percentage}%;"></span>
                    <span class="tooltiptext tooltip-top"></span>
                </div>
                <a href="/product/${item2.id}" class="rating-reviews">(3
                    reviews)</a>
            </div>
            <div class="product-price">
                <ins class="new-price">${OSREC.CurrencyFormatter.format(item2.price, currency)}</ins>
            </div>
        </div>
    </div>` : ''
        z += `</div>`
    }
    return z
}


$(document).on('click', '.category-filter', function (params) {
    let l = $('.category-filter')
    $.each(l, function (i, ele) {
        $(ele).removeClass('current-cat')
    })
    params.preventDefault();
    $('.toolbox-pagination').hide()
    $('.main-content').append('<div class="w-loading"><i></i></div>')
    let i = params.currentTarget;
    $(i).addClass('current-cat')
    let category = i.innerText;

    fetch(`/api/product/product-category/${category}`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json', "X-CSRFToken": Wolmart.getCookie('csrftoken')
        }, body: JSON.stringify({
            max_price: max_num, min_price: min_num
        })
    })
        .then(r => r.json())
        .then(data => {
            setTimeout(function () {
                $('.w-loading').remove();
                history.pushState({}, `${category}`, `/product/product-category/${category}`)
                renderData(data.result, 'shop')
                document.getElementById('shop-grid') && document.getElementById('shop-grid').scrollIntoView(true)
                document.getElementById('shop-list') && document.getElementById('shop-list').scrollIntoView(true)
                data.count && paginate(data)

            }, 5000)
        })

})

$('.go').click(function (e) {
    e.preventDefault();
    $('.main-content').append('<div class="w-loading"><i></i></div>')
    let max_num = Number($(this).closest('.price-range').find('.max_price').val()) !== 0 ? Number($(this).closest('.price-range').find('.max_price').val()) : Number.MAX_SAFE_INTEGER,
        min_num = Number($(this).closest('.price-range').find('.min_price').val()), i = $(this)

    i.addClass("load-more-overlay loading")
    fetch(`/api${window.location.pathname}`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json', "X-CSRFToken": Wolmart.getCookie('csrftoken')
        }, body: JSON.stringify({
            max_price: max_num, min_price: min_num
        })
    })
        .then(r => r.json())
        .then(data => {
            setTimeout(function () {
                i.removeClass("load-more-overlay loading")
                document.querySelector('.w-loading').remove();
                renderData(data.result, 'shop')

                paginate(data)
            }, 5000)

        })
})

function Icon(product, type, shop) {
    let through = type === 'cart' ? JSON.parse(localStorage.getItem('cart')) : Wolmart.getCookie('compare') ? JSON.parse(Wolmart.getCookie('compare')) : [],
        x = type === 'cart' ? '<a href="#" class="btn-product-icon btn-cart w-icon-cart" title="Add to cart"></a>' : '<a href="#" class="btn-product-icon btn-compare w-icon-compare" title="Compare"></a>';

    if (shop) x = ' <a href="#" class="btn-product btn-cart" title="Add to Cart"><i class="w-icon-cart"></i>Add To Cart</a>'
    $.each(through, function (index, value) {
        let p = value['id']
        if (product === p) {
            x = type === 'cart' ? `<a href="#" class="btn-product-icon btn-cart w-icon-minus added" title="remove frm cart"></a>` : `<a href="/compare" class="btn-product-icon btn-compare w-icon-check-solid added" title="Compare"></a>`
            if (shop) x = '<a href="/product/' + value.id + '" class="btn-product btn-cart" title="Add to Cart"><i class="w-icon-cart"></i>Select Options</a>';
        }
    })
    return x
}

fetch(`/api${window.location.pathname}`)
    .then(res => {
        return res.json()
    }).then(data => {
    renderData(data.result, 'shop');
    paginate(data);
})


$(document).on('click', '.pagination-link', function (e) {
    document.querySelector('.main-content').innerHTML += (`
                            <div class="w-loading"><i></i></div>
    `)
    e.preventDefault();
    let i = $(e.currentTarget), url = $(i)[0].getAttribute('ttr')

    fetch(url, {
        method: 'POST', headers: {
            "Content-Type": "application/json", "X-CSRFToken": Wolmart.getCookie('csrftoken')
        }, body: JSON.stringify({
            category: category, range: price
        })
    })
        .then(r => r.json())
        .then(data => {
            setTimeout(function () {
                $('.w-loading').remove()
                renderData(data.result, 'shop')
                paginate(data)

            }, 5000)
        })
}).on('selected', '.pagination-link', function (e) {
    console.log(e)
})


fetch(`/api/catgory/products`)
    .then(r => r.json())
    .then(data => {
        renderData(data, 'index')
    })
