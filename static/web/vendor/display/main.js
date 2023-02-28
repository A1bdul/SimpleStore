let comapre = Wolmart.getCookie('compare') ? JSON.parse(Wolmart.getCookie('compare')) : [],
    cart1 = localStorage.getItem('cart') ? JSON.parse(localStorage.getItem('cart')) : [];


let pk = window.location.pathname.split('/')[2]
if (Number(pk)) {
    document.querySelector('.product').setAttribute('id', pk)
    fetch(`/api/product/details/${pk}`)
        .then(r => r.json())
        .then(data => {
            console.log(data)
            document.querySelectorAll('.product-icon').forEach(form => {
                form.innerHTML += `${Icon(data.product, 'cart', true)}`
            })
            document.querySelectorAll('.product-link-wrapper ').forEach(query => {
                query.innerHTML += `${Icon(data.product, 'compare')}`
            })
            document.querySelectorAll('.brand-logo').forEach(
                brand => brand.setAttribute('src', data.owner.logo)
            ), document.querySelectorAll('.product-name').forEach(
                brand => brand.innerText = data.product['name']
            ), document.querySelectorAll('.product-description').forEach(
                brand => brand.innerHTML = data.product['description']
            )
            for (let i in data.product.image) {
                let image = data.product.image[i]
                document.querySelector('#big-sliderview').innerHTML += `  <div class="swiper-slide">
                                                    <figure class="product-image">
                                                        <img src="${image}"
                                                            data-zoom-image="${image}"
                                                            alt="${data.product.name}" width="800" height="900">
                                                    </figure>
                                                </div>`;
                document.querySelector('#small-sliderview').innerHTML += `<div class="product-thumb swiper-slide">
        <img src="${image}"
            alt="${data.product.name} Thumbnail" width="800" height="900">
    </div>
   `
            }
            document.querySelector('.vendor-products').innerHTML = renderProducts(data['vendor_products'])
            $('.related_products').html(renderProducts(data['related_products']))
        });
function renderProducts(products) {
    let template = "";

    $.each(products, function (index, item) {
        if (item.discount_price) item.discount_price = OSREC.CurrencyFormatter.format(item.discount_price, currency);
        template += (` 
                                    <div class="swiper-slide product" id="${item.id}">
                                        <figure class="product-media">
                                            <a href="/product/${item.id}">
                                                <img src="${item.image[0]}" alt="Product"
                                                     width="300" height="338"/>
                                            </a>
                                            <div class="product-action-vertical">
                                                ${Icon(item, 'cart')}
                                                <a href="#" class="btn-product-icon btn-wishlist w-icon-heart"
                                                   title="Add to wishlist"></a>
                                                   ${Icon(item, 'compare')}
                                            </div>
                                            <div class="product-action">
                                                <a href="#" class="btn-product btn-quickview" title="Quick View">Quick
                                                    View</a>
                                            </div>
                                        </figure>
                                        <div class="product-details">
                                            <div class="product-cat"><a href="/shop">${item.category}</a>
                                            </div>
                                            <h4 class="product-name"><a href="/product/${item.id}">${item.name}</a></h4>
                                            <div class="ratings-container">
                                                <div class="ratings-full">
                                                    <span class="ratings" style="width: 80%;"></span>
                                                    <span class="tooltiptext tooltip-top"></span>
                                                </div>
                                                <a href="/product/${item.id}" class="rating-reviews">(5 reviews)</a>
                                            </div>
                                            <div class="product-pa-wrapper">
                                                <div class="product-price">
                                                    <ins class="new-price">$480.00</ins>
                                                    <del
                                                            class="old-price">$534.00
                                                    </del>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                `)
    })
    return template
}

fetch(`/api/product-comment/${pk}`)
    .then(r => r.json())
    .then(data => {
        console.log(data)
    })
}
fetch('/api/category', {
    headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        "X-CSRFToken": Wolmart.getCookie('csrftoken')
    }
}).then(res => res.json()).then(data => {
    let categoriesmenu = ''
        , categorymobile = ''
        , categoried = "";
    $.each(data, function (index, item) {
        categoried += ` <li><a href="#" class="category-filter">${item.title}</a></li>`;
        categorymobile += item.category_list ? `<li>
                <a href="{% url 'shop' %}">
                    <i class="${item.icon}"></i>${item.title}
                </a>
                <ul>
                    <li>
                        <a href="#">Women</a>
                        <ul>
                            <li><a href="{% url 'shop' %}">New Arrivals</a>
                            </li>
                            <li><a href="{% url 'shop' %}">Best Sellers</a>
                            </li>
                            <li><a href="{% url 'shop' %}">Trending</a></li>
                            <li><a href="{% url 'shop' %}">Clothing</a></li>
                            <li><a href="{% url 'shop' %}">Shoes</a></li>
                            <li><a href="{% url 'shop' %}">Bags</a></li>
                            <li><a href="{% url 'shop' %}">Accessories</a>
                            </li>
                            <li><a href="{% url 'shop' %}">Jewlery &
                                    Watches</a></li>
                            <li><a href="{% url 'shop' %}">Sale</a></li>
                        </ul>
                    </li>
                    <li>
                        <a href="#">Men</a>
                        <ul>
                            <li><a href="{% url 'shop' %}">New Arrivals</a>
                            </li>
                            <li><a href="{% url 'shop' %}">Best Sellers</a>
                            </li>
                            <li><a href="{% url 'shop' %}">Trending</a></li>
                            <li><a href="{% url 'shop' %}">Clothing</a></li>
                            <li><a href="{% url 'shop' %}">Shoes</a></li>
                            <li><a href="{% url 'shop' %}">Bags</a></li>
                            <li><a href="{% url 'shop' %}">Accessories</a>
                            </li>
                            <li><a href="{% url 'shop' %}">Jewlery &
                                    Watches</a></li>
                        </ul>
                    </li>
                </ul>
            </li>` : `<li>
            <a href="{% url 'shop' %}">
                <i class="${item.icon}"></i>${item.title}
            </a>
        </li>`;
        categoriesmenu += item.category_list ? `<li><a href="{% url 'shop' %}"><i class="${item.icon}"></i>${item.title}</a>
                    <ul class="megamenu">${categroytree(item.category_list)}</ul></li>` :
            `<li><a href="{% url 'shop' %}"><i class="${item.icon}"></i>${item.title}</a></li>`;
    });
    $('.filter-category').prepend(categoried)
    $('.category-menu').html(categoriesmenu)
    $('#categorymobile').prepend(categorymobile)
});

function Icon(product, type, shop) {
    let thorugh = type == 'cart' ? JSON.parse(localStorage.getItem('cart')) : comapre
        ,
        x = type == 'cart' ? `<a href="#" class="btn-product-icon btn-cart w-icon-cart" title="Add to cart"></a>` : `<a href="#" class="btn-product-icon btn-compare w-icon-compare" title="Compare"></a>`;
    if (shop) x = ' <a href="#" class="btn-product btn-cart" title="Add to Cart"><i class="w-icon-cart"></i>Add To Cart</a>'
    $.each(thorugh, function (index, value) {
        let p = value['id']
        if (product.id === p) {
            x = type === 'cart' ? `<a href="#" class="btn-product-icon btn-cart w-icon-minus added" title="remove frm cart"></a>` : `<a href="/compare" class="btn-product-icon btn-compare w-icon-check-solid added" title="Compare"></a>`
            if (shop) x = '<a href="/product/${item.id}" class="btn-product btn-cart" title="Add to Cart"><i class="w-icon-cart"></i>Select Options</a>';
        }
    })
    return x
}
