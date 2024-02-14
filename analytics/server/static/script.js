document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('collapse-button').addEventListener('click', function() {
        console.log('Collapse button clicked');
        var buttons = document.getElementsByClassName('nav-button');
        for (var i = 0; i < buttons.length; i++) {
            var text = buttons[i].getElementsByClassName('button-text')[0];
            var icon = buttons[i].getElementsByClassName('button-icon')[0];
            text.classList.toggle('hidden');
            icon.classList.toggle('hidden');
        }
        // Add this line to toggle the 'collapsed' class on the left bar
        document.getElementById('left-bar').classList.toggle('collapsed');
    });
});