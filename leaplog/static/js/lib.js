
// println :: (...any) -> void
const println = (...args) =>
    console.log(...args);

// prinerr :: (...any) -> void
const printerr = (...args) =>
    console.error(...args);

// tuple :: (...any) => [any]
const tuple = (...xs) => [...xs];

// q :: (str, ?Node) -> Node
const q = (selector, parent) =>
    (parent ? parent : document).querySelector(selector);

// q :: (str, ?Node) -> [Node]
const qa = (selector, parent) =>
    (parent ? parent : document).querySelectorAll(selector);

// component :: str -> Node
const component = name =>
    q(`#app .component.${name}`);

const showComponent = name => {
    for (c of qa('#app .component'))
        c.style.display = 'none';
    component(name).style.display = 'block';
}

// pad :: (int, int) -> str
const pad = (times, n) =>
    n > (Math.pow(10, times-1) - 1) ? `${n}` : `${'0'.repeat(times-1)}${n}`;

// elapsed :: int -> int
const elapsed = timestamp =>
    Date.now() - timestamp;

// hours :: int -> [int, int]
const hours = timestamp =>
    tuple(Math.floor(timestamp / 3600000), timestamp % 3600000);

// mins :: int -> [int, int]
const mins = timestamp =>
    tuple(Math.floor(timestamp / 60000), timestamp % 60000);

// secs :: int -> [int, int]
const secs = timestamp =>
    tuple(Math.floor(timestamp / 1000), timestamp % 1000);

// hms :: int -> [int, int, int, int]
function hms(timestamp) {
    const delta = elapsed(timestamp);
    
    const h = hours(delta);
    const m = mins(h[1]);
    const s = secs(m[1]);
    
    const res = {
        values: tuple(h[0], m[0], s[0], s[1]),
        toString() {
            return `
                ${pad(2, this.values[0])}h
                ${pad(2, this.values[1])}m
                ${pad(2, this.values[2])}s
                ${pad(2, Math.floor(this.values[3] / 10).toFixed(0))}`
        }
    }

    return res;
}

// timer :: (str, int, int) => timer
const timer = function(node, time, refresh) {
    if (!(this instanceof timer))
        return new timer();
    
    this.node = node;
    this.time = time;
    this.refresh = refresh;
    this.counter = null;
}

timer.prototype = {
    constructor: timer,

    start() {
        let that = this;
        this.counter = setInterval(
            () => that.draw(),
            that.refresh
        );
    },

    reset(time) { this.time = time; },

    draw() { this.node.textContent = hms(this.time).toString(); },

    stop() { clearInterval(this.counter); }
}

function status() {
    return fetch('/experiment/status')
        .then(response => {
            if (response.code < 200 || response.code > 299)
                throw new Error(response);
            return response.json();
        })
        .then(data => {
            window.runtime = data;
            if (data.error)
                throw new Error(data.error);
            return data;
        }).catch(showError);
}

function showError(err) {
    printerr(err);
    const alert = q('#alert');
    alert.textContent = err;
    alert.style.display = 'block';
    setTimeout(() => { alert.style.display = 'none'; }, 4000)
}

function asyncSubmit(form, handler) {
    return form.on('submit', e => {
        e.preventDefault();
        const destination = form.action;

        fetch(destination, {
            method: 'POST',
            body: new FormData(form)
        }).then(response => {
            if (!response.ok)
                throw Error(response.statusText);
            return response;
        })
        .then(_ => status())
        .then(handler)
        .catch(showError);
    })
}

// Base APIs shortcuts

Node.prototype.on = Node.prototype.addEventListener;