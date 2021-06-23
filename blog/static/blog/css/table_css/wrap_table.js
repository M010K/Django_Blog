[].slice.call(document.querySelectorAll('table')).forEach(function (el) {
    var wrapper = document.createElement('div');
    wrapper.className = 'table100';
    el.parentNode.insertBefore(wrapper, el);
    el.parentNode.removeChild(el);
    wrapper.appendChild(el);
})