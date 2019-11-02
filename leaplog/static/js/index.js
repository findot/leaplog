
(function () {

    window.runtime = {};

    const subject = component('subject');
    const subjectForm = q('form', subject);

    const experiment = component('experiment');
    const experimentForm = q('form', experiment);

    const action = component('action');
    const actionStartForm   = q('form.start-action', action);
    const actionStopForm    = q('form.stop-action', action);
    const actionRemakeForm  = q('form.remake-action', action);


    // DOM Action Bindings

    function reflectStatus(data) {    
        if (data.action_running)
            return showComponent('action');

        if (data.experiment_running)
            return showComponent('experiment');

        return showComponent('subject');
    }

    async_submit(subjectForm, reflectStatus);
    async_submit(experimentForm, reflectStatus);
    async_submit(actionStartForm, reflectStatus);
    async_submit(actionStopForm, reflectStatus);
    async_submit(actionRemakeForm, async_submit);


    // App Entrypoint

    fetch('/experiment/status')
        .then(response => response.json())
        .then(data => {
            window.runtime = data;
            reflectStatus(data)
        }).catch(printerr);

})()