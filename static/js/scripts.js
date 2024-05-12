window.onload = function () {
    if (!window.location.href.includes('form')) {
        return
    }

    // list countries
    var countryDropdown = document.querySelector(".country-dropdown")

    fetch('/get_countries', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            countries = data
            for (var country in countries) {
                var li = document.createElement("li")
                var a = document.createElement("a")
                a.classList.add("dropdown-item")
                a.href = "#"
                a.onclick = (function (country) {
                    return function () {
                        chooseCountry(country, countries[country])
                    }
                })(country);
                a.textContent = countries[country]
                li.appendChild(a)
                countryDropdown.appendChild(li)
            }
        })

    // pagination
    var pages = Array.from(document.querySelectorAll('.page'))
    var breadcrumbs = Array.from(document.querySelectorAll('.breadcrumbs-item'))
    var currentIndex = 0

    pages[currentIndex].classList.add('active')

    var nextButtons = Array.from(document.querySelectorAll('.next-button'))
    nextButtons.forEach(function (button, index) {
        button.addEventListener('click', function () {
            if (pages[currentIndex].querySelector('.input-box').value === '') {
                customAlert('Please fill in the required fields', 'alert-warning')
            }
            else {
                pages[currentIndex].classList.remove('active')
                breadcrumbs[currentIndex].classList.remove('is-active')
                currentIndex++
                if (currentIndex === 5) {
                    pages[currentIndex].classList.add('active')
                    setTimeout(function () {
                        document.querySelector('.form_info').submit()
                    }, 1000)
                } else {
                    pages[currentIndex].classList.add('active')
                    breadcrumbs[currentIndex].classList.add('is-active')
                }
            }
        })
    })

    var backButtons = Array.from(document.querySelectorAll('.back-button'))
    backButtons.forEach(function (button, index) {
        button.addEventListener('click', function () {
            pages[currentIndex].classList.remove('active')
            breadcrumbs[currentIndex].classList.remove('is-active')
            currentIndex--
            pages[currentIndex].classList.add('active')
            breadcrumbs[currentIndex].classList.add('is-active')
        })
    })
}

function chooseCountry(country, name) {
    document.querySelector(".country_btn").innerHTML = name
    document.querySelector(".country_input").value = name
}

function removeDiacritics(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
}

function doFilter(a, filter) {
    var prepared = a.map(function (el) {
        return { target: fuzzysort.prepare(removeDiacritics(el.textContent || el.innerText)), el: el }
    })
    var result = fuzzysort.go(filter, prepared, {
        key: 'target'
    })

    a.forEach(function (el) {
        el.style.display = "none"
    })
    result.forEach(function (res) {
        res.obj.el.style.display = ""
    })
}

function filterCountry() {
    var input = document.querySelector(".country")
    var div = document.querySelector(".country-dropdown")
    var a = Array.from(div.getElementsByTagName("a"))
    doFilter(a, input.value)
}

function customAlert(message, type) {
    var alertContainer = document.querySelector('.alert-container');
    var alertMsg = document.querySelector('.alert-msg');
    alertContainer.classList.add(type)
    alertMsg.innerHTML = message;
    alertContainer.style.display = 'block';

    setTimeout(function () {
        alertContainer.style.display = 'none';
        alertContainer.classList.remove(type)
        alertMsg.innerHTML = "";
    }, 5000);
}