document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.add-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.getAttribute('data-id');
            fetch('/add_to_cart', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({product_id: productId})
            })
            .then(res => res.json())
            .then(data => {
                alert('Added to Cart! 🛒');
            });
        });
    });
});