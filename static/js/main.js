


document.addEventListener('DOMContentLoaded', function () {
    const regionsList = document.getElementById('regionsList');
    const modalBody = document.getElementById('locationModalBody');
    const selectedLabel = document.getElementById('selectedLocationLabel');
    const allBtn = document.getElementById('allUzbekistanBtn');

   
    

    // Клик по области — грузим районы
    regionsList.addEventListener('click', function (e) {
        const btn = e.target.closest('.region-btn');
        if (!btn) return;

        const regionId = btn.dataset.id;
        const regionName = btn.dataset.name;

        fetch(`/locations/get-children/?parent_id=${regionId}`)
            .then(response => response.json())
            .then(districts => {
                showDistricts(regionId, regionName, districts);
            });
    });

    function showDistricts(regionId, regionName, districts) {
        let html = `
            <button type="button" class="btn btn-link mb-2" id="backToRegionsBtn">&larr; Назад к областям</button>
            <button type="button" class="list-group-item list-group-item-action mb-2 select-location-btn" data-id="${regionId}" data-name="${regionName}">
                Весь ${regionName}
            </button>
            <div class="list-group">
        `;
        districts.forEach(d => {
            html += `<button type="button" class="list-group-item list-group-item-action select-location-btn" data-id="${d.id}" data-name="${d.name}">${d.name}</button>`;
        });
        html += `</div>`;

        modalBody.innerHTML = html;

        document.getElementById('backToRegionsBtn').addEventListener('click', resetModal);

        document.querySelectorAll('.select-location-btn').forEach(b => {
            b.addEventListener('click', function () {
                selectLocation(this.dataset.id, this.dataset.name);
            });
        });
    }

    function resetModal() {
        location.reload(); // проще всего — просто перезагрузить модалку в исходное состояние
    }

    function selectLocation(id, name) {
        selectedLabel.textContent = name;
        window.location.href = `/?location=${id}`;
    }

    allBtn.addEventListener('click', function () {
        window.location.href = `/`;
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // ... существующий код ...

    const searchInput = document.getElementById('locationSearchInput');

    searchInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        const items = modalBody.querySelectorAll('.list-group-item');
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(query) ? '' : 'none';
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('shopsContainer');
    const trigger = document.getElementById('scrollTrigger');
    if (!container || !trigger) return;

    let loading = false;

    const observer = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting && !loading) {
            loadMore();
        }
    });
    observer.observe(trigger);

    function loadMore() {
        loading = true;
        const page = container.dataset.nextPage;
        const location = container.dataset.location;
        const category = container.dataset.category || '';
        const query = container.dataset.query || '';
        fetch(`/?page=${page}&location=${location}&category=${category}&q=${encodeURIComponent(query)}&ajax=1`)
        

      
            .then(response => {
                if (response.redirected || !response.ok) {
                    trigger.remove();
                    return null;
                }
                return response.text();
            })
            .then(html => {
                if (!html || html.trim() === '') {
                    trigger.remove();
                    return;
                }
                container.insertAdjacentHTML('beforeend', html);
                container.dataset.nextPage = parseInt(page) + 1;
                loading = false;
            });
    }
});

const categoriesList = document.getElementById('categoriesList');
const categoryModalBody = document.getElementById('categoryModalBody');
const selectedCategoryLabel = document.getElementById('selectedCategoryLabel');
const allCategoriesBtn = document.getElementById('allCategoriesBtn');

function loadCategoryLevel(categoryId, categoryName) {
    fetch(`/categories/get-children/?parent_id=${categoryId}`)
        .then(response => response.json())
        .then(children => {
            if (children.length === 0) {
                window.location.href = `/?category=${categoryId}`;
                return;
            }
            renderCategoryLevel(categoryId, categoryName, children);
        });
}

function renderCategoryLevel(categoryId, categoryName, children) {
    let html = `
        <input type="text" class="form-control mb-3" id="categorySearchInput" placeholder="Поиск...">
        <button type="button" class="btn btn-link mb-2 back-category-btn">&larr; Назад</button>
        <button type="button" class="list-group-item list-group-item-action mb-2 select-category-btn" data-id="${categoryId}">
            Вся категория "${categoryName}"
        </button>
        <div class="list-group">
    `;
    children.forEach(c => {
        html += `<button type="button" class="list-group-item list-group-item-action category-btn" data-id="${c.id}" data-name="${c.name}">${c.name}</button>`;
    });
    html += `</div>`;

    categoryModalBody.innerHTML = html;
    attachCategoryHandlers();
}

function attachCategoryHandlers() {
    categoryModalBody.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            loadCategoryLevel(this.dataset.id, this.dataset.name);
        });
    });

    categoryModalBody.querySelectorAll('.select-category-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            window.location.href = `/?category=${this.dataset.id}`;
        });
    });

    const backBtn = categoryModalBody.querySelector('.back-category-btn');
    if (backBtn) {
        backBtn.addEventListener('click', function () {
            location.reload();
        });
    }
}

if (categoriesList) {
    attachCategoryHandlers();

    if (allCategoriesBtn) {
        allCategoriesBtn.addEventListener('click', function () {
            window.location.href = '/';
        });
    }
}



document.addEventListener('submit', function (e) {
    const form = e.target.closest('.add-to-cart-form');
    if (!form) return;

    e.preventDefault();

    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Товар добавлен в корзину');
                const cartBadge = document.getElementById('cartBadge');
                if (cartBadge) {
                    cartBadge.textContent = data.cart_count;
                    cartBadge.style.display = 'inline-block';
                }
            }
        });
});

function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = 'position:fixed; bottom:20px; right:20px; background:#198754; color:white; padding:12px 20px; border-radius:6px; z-index:9999; box-shadow:0 2px 8px rgba(0,0,0,0.2);';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}