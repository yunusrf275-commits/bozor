

// ===== Модалка "Регион" =====
document.addEventListener('DOMContentLoaded', function () {
    const regionsList = document.getElementById('regionsList');
    const modalBody = document.getElementById('locationModalBody');
    const selectedLabel = document.getElementById('selectedLocationLabel');
    const allBtn = document.getElementById('allUzbekistanBtn');

    if (!regionsList) return;

    function selectLocation(id, name) {
        if (selectedLabel) selectedLabel.textContent = name;
        const params = new URLSearchParams(window.location.search);
        if (id) { params.set('location', id); } else { params.delete('location'); }
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    }

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

    if (allBtn) {
        allBtn.addEventListener('click', function () {
            selectLocation('', 'Весь Узбекистан');
        });
    }

    const searchInput = document.getElementById('locationSearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value.toLowerCase();
            modalBody.querySelectorAll('.list-group-item').forEach(item => {
                item.style.display = item.textContent.toLowerCase().includes(query) ? '' : 'none';
            });
        });
    }
});

// ===== Бесконечная прокрутка (переиспользуется для любой страницы со списком карточек) =====
document.addEventListener('DOMContentLoaded', function () {
    setupInfiniteScroll('shopsContainer', 'scrollTrigger');
    setupInfiniteScroll('listingsContainer', 'listingsScrollTrigger');
});

function setupInfiniteScroll(containerId, triggerId) {
    const container = document.getElementById(containerId);
    const trigger = document.getElementById(triggerId);
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
        const params = new URLSearchParams(window.location.search);
        params.set('page', page);
        params.set('ajax', '1');

        fetch(`${window.location.pathname}?${params.toString()}`)
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
}

// ===== Модалка "Категории" (работает на текущей странице, любая глубина вложенности) =====
document.addEventListener('DOMContentLoaded', function () {
    const categoriesList = document.getElementById('categoriesList');
    const categoryModalBody = document.getElementById('categoryModalBody');
    const allCategoriesBtn = document.getElementById('allCategoriesBtn');

    if (!categoriesList) return;

    function selectCategory(id) {
        const params = new URLSearchParams(window.location.search);
        if (id) { params.set('category', id); } else { params.delete('category'); }
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    }

    function loadCategoryLevel(categoryId, categoryName) {
        fetch(`/categories/get-children/?parent_id=${categoryId}`)
            .then(response => response.json())
            .then(children => {
                if (children.length === 0) {
                    selectCategory(categoryId);
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
                selectCategory(this.dataset.id);
            });
        });

        const backBtn = categoryModalBody.querySelector('.back-category-btn');
        if (backBtn) {
            backBtn.addEventListener('click', function () {
                location.reload();
            });
        }
    }

    attachCategoryHandlers();

    if (allCategoriesBtn) {
        allCategoriesBtn.addEventListener('click', function () {
            selectCategory('');
        });
    }
});

// ===== Добавление в корзину через AJAX =====
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
    toast.className = 'bozor-toast';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

// ===== Каскадный выбор региона в форме подачи объявления =====
document.addEventListener('DOMContentLoaded', function () {
    const regionSelect = document.getElementById('regionSelect');
    const districtSelect = document.getElementById('districtSelect');

    if (!regionSelect || !districtSelect) return;

    regionSelect.addEventListener('change', function () {
        const regionId = this.value;
        districtSelect.innerHTML = '<option value="">Загрузка...</option>';
        districtSelect.disabled = true;

        if (!regionId) {
            districtSelect.innerHTML = '<option value="">Сначала выберите область</option>';
            return;
        }

        fetch(`/locations/get-children/?parent_id=${regionId}`)
            .then(response => response.json())
            .then(districts => {
                districtSelect.innerHTML = '<option value="">Выберите район</option>';
                districts.forEach(d => {
                    const option = document.createElement('option');
                    option.value = d.id;
                    option.textContent = d.name;
                    districtSelect.appendChild(option);
                });
                districtSelect.disabled = false;
            });
    });
});