"use strict";
let comapre = Wolmart.getCookie('compare') ? JSON.parse(Wolmart.getCookie('compare')) : [],
    cart1 = localStorage.getItem('cart') ? JSON.parse(localStorage.getItem('cart')) : [];


fetch('/api/category').then(res => res.json()).then(data => {
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
    let thorugh = type == 'cart' ? JSON.parse(localStorage.getItem('cart')) : Wolmart.getCookie('compare') ? JSON.parse(Wolmart.getCookie('compare')) : []
        ,
        x = type == 'cart' ? `<a href="#" class="btn-product-icon btn-cart w-icon-cart" title="Add to cart"></a>` : `<a href="#" class="btn-product-icon btn-compare w-icon-compare" title="Compare"></a>`;
    if (shop) x = ' <a href="#" class="btn-product btn-cart" title="Add to Cart"><i class="w-icon-cart"></i>Add To Cart</a>'
    $.each(thorugh, function (index, value) {
        let p = value['id']
        console.log(p, product, typeof p, typeof product)
        if (product === p) {
            x = type === 'cart' ? `<a href="#" class="btn-product-icon btn-cart w-icon-minus added" title="remove frm cart"></a>` : `<a href="/compare" class="btn-product-icon btn-compare w-icon-check-solid added" title="Compare"></a>`
            if (shop) x = '<a href="/product/${item.id}" class="btn-product btn-cart" title="Add to Cart"><i class="w-icon-cart"></i>Select Options</a>';
        }
    })
    return x
}
