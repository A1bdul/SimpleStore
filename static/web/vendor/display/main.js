function Icon(product, type, shop) {
    let thorugh = type == 'cart' ? JSON.parse(localStorage.getItem('cart')) : Wolmart.getCookie('compare') ? JSON.parse(Wolmart.getCookie('compare')) : []
        ,
        x = type == 'cart' ? `<a href="#" class="btn-product-icon btn-cart w-icon-cart" title="Add to cart"></a>` : `<a href="#" class="btn-product-icon btn-compare w-icon-compare" title="Compare"></a>`;
    if (shop) x = ' <a href="#" class="btn-product btn-cart" title="Add to Cart"><i class="w-icon-cart"></i>Add To Cart</a>'
    $.each(thorugh, function (index, value) {
        let p = value['id']
        console.log(p, product, typeof p, typeof product)
        if (product === p) {
            x = type == 'cart' ? `<a href="#" class="btn-product-icon btn-cart w-icon-minus added" title="remove frm cart"></a>` : `<a href="compare" class="btn-product-icon btn-compare w-icon-check-solid added" title="Compare"></a>`
            if (shop) x = '<a href="/product/${item.id}" class="btn-product btn-cart" title="Add to Cart"><i class="w-icon-cart"></i>Select Options</a>';
        }
    })
    return x
}
