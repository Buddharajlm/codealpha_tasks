/**
 * ShopZone - JavaScript Helper Engine
 * Pure Vanilla JavaScript for Shopping Cart, Notifications & Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    initToastContainer();
    initAjaxAddToCart();
    initAlertDismissal();
    initQuantitySteppers();
    initCartQuantityAdjusters();
});

/**
 * Toast Notification System
 */
function initToastContainer() {
    if (!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let icon = '✅';
    if (type === 'error') icon = '❌';
    if (type === 'info') icon = 'ℹ️';

    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

/**
 * AJAX Add To Cart Handling
 */
function initAjaxAddToCart() {
    const cartForms = document.querySelectorAll('.ajax-cart-form');

    cartForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;

            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span>Adding...</span>';

            const formData = new FormData(form);
            const url = form.getAttribute('action');

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    // Update badge
                    const badges = document.querySelectorAll('.cart-count');
                    badges.forEach(b => {
                        b.textContent = data.total_items;
                        b.style.transform = 'scale(1.3)';
                        setTimeout(() => b.style.transform = 'scale(1)', 200);
                    });

                    showToast(data.message || 'Item added to your cart!', 'success');
                } else {
                    const err = await response.json();
                    showToast(err.message || 'Failed to add item.', 'error');
                }
            } catch (error) {
                console.error('Cart Error:', error);
                // Fallback to normal form submit if fetch fails
                form.submit();
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        });
    });
}

/**
 * Stepper buttons on Product Details
 */
function initQuantitySteppers() {
    const decBtns = document.querySelectorAll('.qty-decrement');
    const incBtns = document.querySelectorAll('.qty-increment');

    decBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.closest('.qty-stepper').querySelector('.qty-input');
            const min = parseInt(input.getAttribute('min') || '1', 10);
            let val = parseInt(input.value || '1', 10);
            if (val > min) {
                input.value = val - 1;
            }
        });
    });

    incBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.closest('.qty-stepper').querySelector('.qty-input');
            const max = parseInt(input.getAttribute('max') || '99', 10);
            let val = parseInt(input.value || '1', 10);
            if (val < max) {
                input.value = val + 1;
            }
        });
    });
}

/**
 * Cart page quantity updates via AJAX
 */
function initCartQuantityAdjusters() {
    const updateForms = document.querySelectorAll('.cart-item-update-form');

    updateForms.forEach(form => {
        const input = form.querySelector('.cart-qty-input');
        if (!input) return;

        input.addEventListener('change', () => {
            form.submit();
        });
    });
}

/**
 * Alert Dismissal
 */
function initAlertDismissal() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 250);
            });
        }

        // Auto dismiss after 5s
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 250);
            }
        }, 5000);
    });
}

/**
 * Print receipt helper
 */
function printReceipt() {
    window.print();
}
