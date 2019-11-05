
(function () {

    window.runtime          = {};

    const alert             = q('#alert');
    if (alert.textContent == '')
        alert.style.display     = 'none';

    if (window.runtime.error) {
        for (b of qa('button'))
            b.disabled = true;
        alert.textContent = window.runtime.error;
        alert.style.display = block;
    }

    const subject           = component('subject');
    const subjectForm       = q('form', subject);

    const experiment        = component('experiment');
    const experimentForm    = q('form', experiment);

    const action            = component('action');
    // const actionStartForm   = q('form.start-action', action);
    // const actionStopForm    = q('form.stop-action', action);
    const actionToggleForm  = q('form.toggle-action', action);
    const actionRemakeForm  = q('form.remake-action', action);
    const actionNextForm    = q('form.next-action', action);
    
    const actionNumber      = q('.action-number', action)
    const actionTimer       = new timer(q('.timer', action), null, 50);

    // DOM Action Bindings

    function reflectStatus(data) {
        if (!data)
            return;

        if (data.experiment_running || data.action_running) {
            actionNumber.textContent = `Action n°${data.action.reference}`;
            if (data.action_running) {                
                q('.toggle-stop', actionToggleForm).style.display = 'block';
                q('.toggle-start', actionToggleForm).style.display = 'none';
                actionTimer.time = new Date().getTime();
                actionTimer.start();
            } else {
                q('.toggle-stop', actionToggleForm).style.display = 'none';
                q('.toggle-start', actionToggleForm).style.display = 'block';
                actionTimer.stop();
            }
            return showComponent('action');
        }

        if (data.subject_registered)
            return showComponent('experiment');

        return showComponent('subject');
    }

    asyncSubmit(subjectForm, reflectStatus);
    asyncSubmit(experimentForm, reflectStatus);
    //asyncSubmit(actionStartForm, reflectStatus);
    //asyncSubmit(actionStopForm, reflectStatus);
    asyncSubmit(actionToggleForm, reflectStatus);
    asyncSubmit(actionNextForm, reflectStatus);
    asyncSubmit(actionRemakeForm, reflectStatus)
    actionNextForm.on('click', _ => {
        actionTimer.reset(new Date());
        actionTimer.draw();
    })
    actionRemakeForm.on('click', _ => {
        actionTimer.reset(new Date());
        actionTimer.draw();
    });

    // App Entrypoint

    status().then(reflectStatus);

})()
