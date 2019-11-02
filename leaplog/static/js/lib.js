
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

// pad2 :: int -> str
const pad2 = n =>
    (n > 9 ? '' : '0') + n;

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
    
    const res = tuple(h[0], m[0], s[0], s[1]);
    res.toString = function() {
        return `${pad2(this[0])}h ${pad2(this[1])}m ${pad2(this[2])}s${this[3]}`
    }
    
    return res
}

// timer :: (str, int, int) => timer
const timer = function(selector, start, refresh) {
    if (!(this instanceof timer))
        return new timer();
    
    this.node = q(selector);
    this.start = start;
    this.refresh = refresh;
    this.counter = null;
}

timer.prototype = {
    constructor: timer,
    
    start() {
        this.counter = setTimeout(
            () => this.node.textContent = hms(timestamp).toString(),
            this.refresh
        );
    },
    
    stop() { clearTimeout(this.counter); }
}

function async_submit(form, handler) {
    form.on('submit', e => {
        e.preventDefault();
        const destination = form.action;

        fetch(destination, {
            method: 'POST',
            body: new FormData(form)
        })
        .then(_ => fetch('/experiment/status'))
        .then(response => response.json())
        .then(handler);
    })
}

// Base APIs shortcuts

Node.prototype.on = Node.prototype.addEventListener;